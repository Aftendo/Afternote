"""
ugo.py
Conversion by ChatGPT

Based off jaames and sudofox class.ugomenu.php: https://github.com/Sudomemo/sudomemo-utils/blob/master/php/class.ugomenu.php

"""
import base64
import os
import struct

class UgoMenu:
    def __init__(self):
        self.types = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "index": "0",
            "small_list": "1",
            "grid": "2",
            "list": "4",
        }
        self.meta = {}
        self.menu = {}
        self.embeds = []

    def write_label(self, text):
        return base64.b64encode(text.encode("utf-16le")).decode()

    def set_type(self, value):
        self.meta["type"] = self.types[value]

    def set_meta(self, value, text):
        self.meta[value.lower()] = text

    def add_dropdown(self, args):
        if "dropdown" not in self.menu:
            self.menu["dropdown"] = []
        self.menu["dropdown"].append(
            {
                "url": args.get("url", ""),
                "label": args.get("label", ""),
                "selected": args.get("selected", "0"),
            }
        )

    def add_button(self, args):
        if "button" not in self.menu:
            self.menu["button"] = []
        self.menu["button"].append(
            {
                "url": args.get("url", ""),
                "label": args.get("label", ""),
            }
        )

    def add_item(self, args, should_replace_icon=True):
        if "item" not in self.menu:
            self.menu["item"] = []
        if "file" in args:
            self.add_file(args["file"])
            if should_replace_icon:
                args["icon"] = str(len(self.embeds) - 1)
        self.menu["item"].append(
            {
                "url": args.get("url", ""),
                "label": args.get("label", ""),
                "icon": args.get("icon", "104"),
                "counter": args.get("counter", ""),
                "lock": args.get("lock", ""),
                "unknown": args.get("unknown", "0"),
            }
        )

    def add_file(self, path):
        self.embeds.append(
            {
                "ext": os.path.splitext(path)[1][1:],
                "path": path,
            }
        )

    def get_ugo(self):
        ret = b""
        section_table = []
        menu_data = []

        # TYPE 0 -- LAYOUT TYPE
        menu_data.append(b"0\t" + (self.meta.get("type", "4")).encode())

        # TYPE 1 -- TOP SCREEN LAYOUT
        if "upperlink" in self.meta:
            menu_data.append(
                b"1\t1\t" + self.meta["upperlink"].encode()
            )
        else:
            menu_data.append(
                b"1\t0\t"
                + self.write_label(self.meta.get("uppertitle", "")).encode()
                + b"\t"
                + self.write_label(self.meta.get("uppersubleft", "")).encode()
                + b"\t"
                + self.write_label(self.meta.get("uppersubright", "")).encode()
                + b"\t"
                + self.write_label(self.meta.get("uppersubtop", "")).encode()
                + b"\t"
                + self.write_label(self.meta.get("uppersubbottom", "")).encode()
            )

        # TYPE 2 -- DROPDOWN ITEMS
        if "dropdown" in self.menu:
            for item in self.menu["dropdown"]:
                menu_data.append(
                    b"2\t"
                    + item.get("url", b"").encode()
                    + b"\t"
                    + self.write_label(item.get("label", "")).encode()
                    + b"\t"
                    + item.get("selected", b"0").encode()
                )

        # TYPE 3 -- BUTTONS
        if "button" in self.menu:
            for item in self.menu["button"]:
                menu_data.append(
                    b"3\t" + item.get("url", b"").encode() + b"\t" + self.write_label(item.get("label", "")).encode()
                )
        # TYPE 4 -- ITEMS
        if "item" in self.menu:
            for item in self.menu["item"]:
                #dirty fix
                if isinstance(item.get("icon"), int):
                    icon = "104"
                else:
                    icon = item.get("icon")
                menu_data.append(
                    b"4\t"
                    + item.get("url", b"").encode()
                    + b"\t"
                    + icon.encode()
                    + b"\t"
                    + self.write_label(item.get("label", "")).encode()
                    + b"\t"
                    + item.get("counter", b"").encode()
                    + b"\t"
                    + item.get("lock", b"").encode()
                    + b"\t"
                    + item.get("unknown", b"0").encode()
                )

        # join all the items using newlines
        menu_data = b"\n".join(menu_data)

        # HEADER
        # get the byte length of this section and add it to the section table
        menu_data_len = len(menu_data)
        section_table.append(menu_data_len)

        # pad the actual length to the nearest multiple of four
        menu_data = menu_data.ljust((menu_data_len + 3) // 4 * 4, b"\0")

        # calculate the embed section length
        embed_len = False
        if len(self.embeds) > 0:
            embed_len = 0
            for item in self.embeds:
                # .ppm is 1696 bytes while ntft is 2024
                embed_len += 1696 if item["ext"] == "ppm" else 2048
            # add this length to the section table
            section_table.append(embed_len)

        # write the magic ('UGAR') and number of sections
        ret += struct.pack(f"4sI", b"UGAR", len(section_table))

        # write the length of each section
        ret += struct.pack(f"{len(section_table)}I", *section_table)

        # append the menu data
        ret += menu_data

        # EMBEDS
        if embed_len is not False:
            for item in self.embeds:
                # check that the file exists
                if not os.path.exists(item["path"]):
                    filename = item["path"]
                    print(f"Error generating Ugomenu: could not open file {filename}")
                    exit()
                # open the file
                with open(item["path"], "rb") as file:
                    if item["ext"] == "ppm":
                        ret += file.read(1696)
                    elif item["ext"] == "ntft":
                        ret += file.read(2048)

        return ret

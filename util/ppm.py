# ========================================
# ppm.py version 1.0.0, fork for AfterNote
# ========================================

# Class for parsing Flipnote Studio's .ppm animation format
# Implementation by James Daniel (aka jaames) (github.com/jaames | rakujira.jp)
# Modified by Rixy for Afternote purposes, original code available at https://
#
# Credits:
#   PPM format reverse-engineering and documentation:
#     bricklife (http://ugomemo.g.hatena.ne.jp/bricklife/20090307/1236391313)
#     mirai-iro (http://mirai-iro.hatenablog.jp/entry/20090116/ugomemo_ppm)
#     harimau_tigris (http://ugomemo.g.hatena.ne.jp/harimau_tigris)
#     steven (http://www.dsibrew.org/wiki/User:Steven)
#     yellows8 (http://www.dsibrew.org/wiki/User:Yellows8)
#     PBSDS (https://github.com/pbsds)
#     jaames (https://github.com/jaames)
#   Identifying the PPM sound codec:
#     Midmad from Hatena Haiku
#     WDLMaster from hcs64.com

import struct
import numpy as np
from datetime import datetime 

class PPMParser:
  @classmethod
  def open(cls, path):
    f = open(path, "rb")
    return cls(f)

  def __init__(self, stream=None):
    if stream: self.load(stream)

  def load(self, stream):
    self.stream = stream
    self.read_header()
    if self.magic != b'PARA':
      return False
    self.read_meta()
    return True
  
  def unload(self):
    self.stream.close()

  def read_header(self):
    # decode header
    # https://github.com/pbsds/hatena-server/wiki/PPM-format#file-header
    self.stream.seek(0)
    magic, animation_data_size, sound_data_size, frame_count, version = struct.unpack("<4sIIHH", self.stream.read(16))
    self.magic = magic
    self.animation_data_size = animation_data_size
    self.sound_data_size = sound_data_size
    self.frame_count = frame_count + 1

  def read_filename(self):
    # Parent and current filenames are stored as:
    #  - 3 bytes representing the last 6 digits of the Consoles's MAC address
    #  - 13-character string
    #  - uint16 edit counter
    mac, ident, edits = struct.unpack("<3s13sH", self.stream.read(18));
    # Filenames are formatted as <3-byte MAC as hex>_<13-character string>_<edit counter as a 3-digit number>
    # eg F78DA8_14768882B56B8_030
    return "{0}_{1}_{2:03d}".format("".join(["%02X" % c for c in mac]), ident.decode("ascii"), edits)
    
  def read_meta(self):
    # decode metadata
    # https://github.com/pbsds/hatena-server/wiki/PPM-format#file-header
    self.stream.seek(0x10)
    self.lock, self.thumb_index = struct.unpack("<HH", self.stream.read(4))
    self.root_author_name = self.stream.read(22).decode("utf-16").rstrip("\x00")
    self.parent_author_name = self.stream.read(22).decode("utf-16").rstrip("\x00")
    self.current_author_name = self.stream.read(22).decode("utf-16").rstrip("\x00")
    self.parent_author_id = "%016X" % struct.unpack("<Q", self.stream.read(8))
    self.current_author_id = "%016X" % struct.unpack("<Q", self.stream.read(8))
    self.parent_filename = self.read_filename()
    self.current_filename = self.read_filename()
    self.root_author_id = "%016X" % struct.unpack("<Q", self.stream.read(8))
    self.partial_filename = self.stream.read(8) # not really useful for anything :/
    # timestamp is stored as the number of seconds since jan 1st 2000
    timestamp = struct.unpack("<I", self.stream.read(4))[0]
    # we add 946684800 to convert this to a more common unix timestamp, which start on jan 1st 1970
    self.timestamp = datetime.fromtimestamp(timestamp + 946684800)

  def get_filename(self):
    return self.current_filename

  def read_thumbnail(self):
    self.stream.seek(0xA0)
    bitmap = np.zeros((48, 64), dtype=np.uint8)
    for tile_index in range(0, 48):
      tile_x = tile_index % 8 * 8
      tile_y = tile_index // 8 * 8
      for line in range(0, 8):
        for pixel in range(0, 8, 2):
          byte = ord(self.stream.read(1))
          x = tile_x + pixel
          y = tile_y + line
          bitmap[y][x] = byte & 0x0F
          bitmap[y][x + 1] = (byte >> 4) & 0x0F
    return bitmap
  def get_tmb(self):
    self.stream.seek(0)
    return self.stream.read(1696)
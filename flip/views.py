from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from util.ugo import UgoMenu
from util.ppm import PPMParser
import os.path, io
from db.models import *

@csrf_exempt
def auth(request, reg):
    #resp = HttpResponse("Yo mama so stupid,\nthat you got banned off Afternote", content_type="text/plain; charset=utf-16le")
    resp = HttpResponse()
    resp.headers['X-DSi-Auth-Challenge'] = 'aftendoo'
    resp.headers['X-DSi-SID'] = 'TestSession'
    resp.headers['X-DSi-New-Notices'] = 0
    resp.headers['X-DSi-Unread-Notices'] = 0
    #resp.headers['X-DSi-Dialog-Type'] = 1
    return resp

@csrf_exempt
def content(request, reg, country, file):
    if os.path.exists("./cfg/"+file+".txt"):
        with open("./cfg/"+file+".txt", "r+") as file:
            return HttpResponse(file.read(), content_type='text/plain; charset=utf-16le')
    else:
        return HttpResponse("WARNING: cfg/"+file+".txt does not exists.", content_type='text/plain; charset=utf-16le')

@csrf_exempt
def eula_list(request, reg):
    return HttpResponse("RQBuAGcAbABpAHMAaAA=	en", content_type='text/plain; charset=utf-16le')

@csrf_exempt
def index(request, reg):
    ugo = UgoMenu()
    ugo.set_type("0")
    ugo.add_item({"label": "Hot Flipnotes", "url": request.build_absolute_uri('/')+"ds/v2-eu/hot.uls", "icon": "104"})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def ugo_list(request, reg):
    flips = Flipnote.objects.all().order_by("-id")
    ugo = UgoMenu()
    ugo.set_type("2")
    ugo.set_meta("uppertitle", "Hot Flipnotes")
    ugo.add_button({"label": "Post here", "url": request.build_absolute_uri('/')+"ds/v2-eu/post/flipnote.post"})
    for flip in flips:
        if os.path.exists("./files/ppm/"+flip.real_filename+".ppm"):
            with open("./files/ppm/"+flip.real_filename+".ppm", "rb+") as file:
                parser = PPMParser()
                if parser.load(file):
                    ugo.add_item({"url": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+parser.current_filename+".ppm", "file": "./files/ppm/"+parser.current_filename+".ppm"})
                else:
                    continue
        else:
            continue
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def info(request, reg, file):
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    flip.views += 1
    flip.save()
    return HttpResponse("0\n0\n", content_type="text/plain; charset=utf-16le")

@csrf_exempt
def dl(request, reg, file):
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    flip.saved += 1
    flip.save()
    return HttpResponse("nice", content_type="text/plain; charset=utf-16le")

@csrf_exempt
def flipnote_info(request, reg, file):
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    return render(request, "details.html", {"flipnote": flip, "ppmUri": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+file+".ppm"}, content_type="text/html; charset=utf-8")
    
@csrf_exempt
def ppmloader(request, reg, file):
    if os.path.exists("./files/ppm/"+file+".ppm"):
        with open("./files/ppm/"+file+".ppm", "rb+") as file:
            return HttpResponse(file.read(), content_type="text/plain; charset=utf-16le")
    else:
        resp = HttpResponse()
        resp.status_code = 404
        return resp

@csrf_exempt
def post_flip(request, reg):
    if request.method == 'POST':
        if request.body != "":
            parser = PPMParser()
            if parser.load(io.BytesIO(request.body)):
                try:
                    Flipnote.objects.get(real_filename=parser.current_filename)
                    return HttpResponse()
                except ObjectDoesNotExist:
                    pass
                with open("./files/ppm/"+parser.current_filename+".ppm", "wb") as file:
                    file.write(request.body)
                    file.close()
                Flipnote.objects.create(real_filename=parser.current_filename)
                return HttpResponse()
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)
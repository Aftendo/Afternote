from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from util.ugo import UgoMenu
from util.ppm import PPMParser
import os.path, io, random, string
from django.contrib.auth import authenticate
from db.models import *

@csrf_exempt
def auth(request, reg):
    resp = HttpResponse(content_type="text/plain; charset=utf-16le")
    if "X-DSi-SID" in request.headers and "X-DSi-MAC" in request.headers and "X-DSi-ID" in request.headers:
        resp.headers['X-DSi-SID'] = 'nobitches?'
        resp.headers['X-DSi-New-Notices'] = 0
        resp.headers['X-DSi-Unread-Notices'] = 0
        try:
            session = Session.objects.get(token=request.headers['X-DSi-SID'])
            session.fsid = request.headers['X-DSi-ID']
            session.mac = request.headers['X-DSi-MAC']
            session.save()
        except:
            resp.headers['X-DSi-Dialog-Type'] = 1
            resp.write("Invalid Session. Please reboot the app.")
            return resp
        try:
            user = User.objects.get(fsid=request.headers['X-DSi-ID'], mac=request.headers['X-DSi-MAC'])
            sessions = Session.objects.filter(user=user).delete()
            if user.ban:
                resp.headers['X-DSi-Dialog-Type'] = 1
                resp.write("Yo mama so stupid,\nthat you got banned off Afternote")
                return resp
            session.user = user
            session.save()
        except ObjectDoesNotExist:
            pass
    else:
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        Session.objects.create(token=token)
        resp.headers['X-DSi-Auth-Challenge'] = 'aftendoo'
        resp.headers['X-DSi-SID'] = token
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
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    ugo = UgoMenu()
    ugo.set_type("0")
    if session.user != None:
        ugo.add_item({"label": "All Flipnotes", "url": request.build_absolute_uri('/')+"ds/v2-eu/newest.uls", "icon": "100"})
        ugo.add_item({"label": "Channels", "url": request.build_absolute_uri('/')+"ds/v2-eu/channels.uls", "icon": "101"})
    else:    
        ugo.add_item({"label": "Sign In", "url": request.build_absolute_uri('/')+"ds/v2-eu/signin.htm", "icon": "104"})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def categories(request, reg):
    categories = Category.objects.all()[:8]
    ugo = UgoMenu()
    ugo.set_type("0")
    for category in categories:
        ugo.add_item({"label": category.name, "url": request.build_absolute_uri('/')+"ds/v2-eu/channels/"+category.internal_id+".uls"})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def channels(request, reg, internal_id):
    try:
        category = Category.objects.get(internal_id=internal_id)
    except:
        return HttpResponse(status=403)
    channels = Channel.objects.filter(category=category)
    ugo = UgoMenu()
    ugo.set_meta("uppertitle", category.name)
    ugo.set_type("1")
    for channel in channels:
        ugo.add_item({"label": channel.name, "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".uls"})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def others(request, reg):
    categories = Category.objects.all()[8:]
    ugo = UgoMenu()
    ugo.set_meta("uppertitle", "Other channels")
    ugo.set_type("1")
    for category in categories:
        ugo.add_item({"label": category.name, "url": request.build_absolute_uri('/')+"ds/v2-eu/channels/"+category.internal_id+".uls"})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def channel(request, reg, internal_id):
    try:
        channel = Channel.objects.get(internal_id=internal_id)
    except:
        return HttpResponse(status=403)
    if not request.GET.get("page"):
        page = 0
    else:
        page = int(request.GET.get("page"))
    flip_count = Flipnote.objects.filter(channel=channel).count()
    flips = Flipnote.objects.filter(channel=channel).order_by("-id")[page*50:50]    
    ugo = UgoMenu()
    ugo.set_type("2")
    ugo.set_meta("uppertitle", channel.name)
    ugo.set_meta("uppersubleft", "Flipnotes")
    ugo.set_meta("uppersubright", str(flip_count))
    ugo.add_button({"label": "Post here", "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".post"})
    if page != 0:
        ugo.add_item({"label": "Previous", "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".uls?page="+str(page-1)})
    for flip in flips:
        if os.path.exists("./files/ppm/"+flip.real_filename+".ppm"):
            with open("./files/ppm/"+flip.real_filename+".ppm", "rb+") as file:
                parser = PPMParser()
                if parser.load(file):
                    ugo.add_item({"url": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+parser.current_filename+".ppm", "file": "./files/ppm/"+parser.current_filename+".ppm", "lock": str(flip.is_locked)})
                else:
                    continue
        else:
            continue
    if flip_count > (page+1)*50:
        ugo.add_item({"label": "Next", "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".uls?page="+str(page+1)})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def signin(request, reg):
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    if request.GET.get("finish"):
        return render(request, "signin/finish.html")    
    elif not request.GET.get("step2"):
        return render(request, "signin/step1.html", {"BASE_URI": request.build_absolute_uri('/')})
    else:
        return render(request, "signin/step2.html", {"BASE_URI": request.build_absolute_uri('/')})

@csrf_exempt
def signin_step1(request, reg):
    try:
        session = Session.objects.get(token=request.headers['X-Dsi-Sid'])
    except:
        return HttpResponse(status=403)
    resp = HttpResponse()
    if request.method == 'POST':
        if request.headers['X-Email-Addr'] != "":
            try:
                user = User.objects.get(username=request.headers['X-Email-Addr'])
                session.temp = user.username
                session.save()
                resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/signin.htm?step2=true"
            except ObjectDoesNotExist:
                resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/error_get.htm?error=Invalid+username"
        else:
            resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/error_get.htm?error=Empty+username+please+try+again"
    else:
        resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/error_get.htm?error=An+error+has+occured."
    return resp
    
@csrf_exempt
def signin_step2(request, reg):
    try:
        session = Session.objects.get(token=request.headers['X-Dsi-Sid'])
    except:
        return HttpResponse(status=403)
    resp = HttpResponse()
    if request.method == 'POST':
        if request.headers['X-Email-Addr'] != "":
            user = authenticate(username=session.temp, password=request.headers['X-Email-Addr'])
            if user != None:
                try:
                    test = User.objects.get(fsid=session.fsid)
                    test.fsid = None
                    test.save()
                except ObjectDoesNotExist:
                    pass
                try:
                    test = User.objects.get(mac=session.mac)
                    test.mac = None
                    test.save()
                except ObjectDoesNotExist:
                    pass
                user = User.objects.get(username=session.temp)
                user.fsid = session.fsid
                user.mac = session.mac
                user.save()
                resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/signin.htm?finish=true"
            else:
                resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/error_get.htm?error=Invalid+password+please+try+again"
        else:
            resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/error_get.htm?error=Empty+password+please+try+again"
    else:
        resp.headers['X-DSi-Forwarder'] = request.build_absolute_uri('/')+"ds/v2-eu/error_get.htm?error=An+error+has+occured."
    return resp

@csrf_exempt
def error_get(request, reg):
    return render(request, "error.html", {"errMsg": request.GET.get("error")})

@csrf_exempt
def newest_list(request, reg):
    if not request.GET.get("page"):
        page = 0
    else:
        page = int(request.GET.get("page"))
    flip_count = Flipnote.objects.all().count()
    flips = Flipnote.objects.all().order_by("-id")[page*50:50]
    ugo = UgoMenu()
    ugo.set_type("2")
    ugo.set_meta("uppertitle", "All Flipnotes")
    ugo.set_meta("uppersubleft", "Flipnotes")
    ugo.set_meta("uppersubright", str(flip_count))
    if page != 0:
        ugo.add_item({"label": "Previous", "url": request.build_absolute_uri('/')+"ds/v2-eu/newest.uls?page="+str(page-1)})
    for flip in flips:
        if os.path.exists("./files/ppm/"+flip.real_filename+".ppm"):
            with open("./files/ppm/"+flip.real_filename+".ppm", "rb+") as file:
                parser = PPMParser()
                if parser.load(file):
                    ugo.add_item({"url": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+parser.current_filename+".ppm", "file": "./files/ppm/"+parser.current_filename+".ppm", "lock": str(flip.is_locked)})
                else:
                    continue
        else:
            continue
    if flip_count > (page+1)*50:
        ugo.add_item({"label": "Next", "url": request.build_absolute_uri('/')+"ds/v2-eu/newest.uls?page="+str(page+1)})
    return HttpResponse(ugo.get_ugo(), content_type="text/plain; charset=utf-16le")

@csrf_exempt
def info(request, reg, file):
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    if session.user != flip.made_by:
        flip.views += 1
        flip.save()
    return HttpResponse("0\n0\n", content_type="text/plain; charset=utf-16le")

@csrf_exempt
def dl(request, reg, file):
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    if session.user != flip.made_by:
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
def post_flip(request, reg, internal_id):
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    try:
        channel = Channel.objects.get(internal_id=internal_id)
    except:
        return HttpResponse(status=403)
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
                if parser.lock < 0 or parser.lock > 1:
                    return HttpResponse(status=403)
                Flipnote.objects.create(real_filename=parser.current_filename, is_locked=parser.lock, made_by=session.user, channel=channel)
                return HttpResponse()
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)
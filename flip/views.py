from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from util.ugo import UgoMenu
from util.ppm import PPMParser
import os.path, io, random, string, datetime
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
        ugo.add_item({"label": "Browse Flipnotes", "url": request.build_absolute_uri('/')+"ds/v2-eu/hot.uls", "icon": "100"})
        ugo.add_item({"label": "Channels", "url": request.build_absolute_uri('/')+"ds/v2-eu/channels.uls", "icon": "101"})
    else:    
        ugo.add_item({"label": "Sign In", "url": request.build_absolute_uri('/')+"ds/v2-eu/signin.htm", "icon": "104"})
    return HttpResponse(ugo.get_ugo())

@csrf_exempt
def categories(request, reg):
    categories = Category.objects.all()[:8]
    ugo = UgoMenu()
    ugo.set_type("0")
    for category in categories:
        ugo.add_item({"label": category.name, "url": request.build_absolute_uri('/')+"ds/v2-eu/channels/"+category.internal_id+".uls"})
    return HttpResponse(ugo.get_ugo())

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
    return HttpResponse(ugo.get_ugo())

@csrf_exempt
def others(request, reg):
    categories = Category.objects.all()[8:]
    ugo = UgoMenu()
    ugo.set_meta("uppertitle", "Other channels")
    ugo.set_type("1")
    for category in categories:
        ugo.add_item({"label": category.name, "url": request.build_absolute_uri('/')+"ds/v2-eu/channels/"+category.internal_id+".uls"})
    return HttpResponse(ugo.get_ugo())

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
    if not channel.locked:
        ugo.add_button({"label": "Post here", "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".post"})
    if page != 0:
        ugo.add_item({"label": "Previous", "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".uls?page="+str(page-1)})
    for flip in flips:
        if os.path.exists("./files/ppm/"+flip.real_filename+".ppm"):
            with open("./files/ppm/"+flip.real_filename+".ppm", "rb+") as file:
                parser = PPMParser()
                if parser.load(file):
                    ugo.add_item({"url": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+parser.current_filename+".ppm", "file": "./files/ppm/"+parser.current_filename+".ppm", "lock": str(flip.is_locked), "counter": str(flip.star+flip.green_star+flip.red_star+flip.blue_star+flip.purple_star), "icon": "3"}, False)
                else:
                    continue
        else:
            continue
    if flip_count > (page+1)*50:
        ugo.add_item({"label": "Next", "url": request.build_absolute_uri('/')+"ds/v2-eu/channel/"+channel.internal_id+".uls?page="+str(page+1)})
    return HttpResponse(ugo.get_ugo())

@csrf_exempt
def newest_list(request, reg):
    return flip_list(request, True)

@csrf_exempt
def popular_list(request, reg):
    return flip_list(request, None)

@csrf_exempt
def liked_list(request, reg):
    return flip_list(request, False)

"""
type argument: None is Popular Flipnotes, False is Most Liked, and True is New Flipnotes
"""
@csrf_exempt
def flip_list(request, type=None):
    if not request.GET.get("page"):
        page = 0
    else:
        page = int(request.GET.get("page"))
    flip_count = Flipnote.objects.all().count()
    ugo = UgoMenu()
    ugo.set_type("2")
    if type==None:
        ugo.set_meta("uppertitle", "Popular Flipnotes")
        ugo.set_meta("uppersubbottom", "The most popular recent flipnotes.")
        flips = Flipnote.objects.all().order_by("-views")[page*50:50]
        selected_newest = "0"
        selected_popular = "1"
        selected_liked = "0"
    elif type==False:
        ugo.set_meta("uppertitle", "Liked Flipnotes")
        ugo.set_meta("uppersubbottom", "The most liked recent flipnotes.")
        flips = Flipnote.objects.all().order_by("-total")[page*50:50]
        selected_newest = "0"
        selected_popular = "0"
        selected_liked = "1"
    elif type==True:
        ugo.set_meta("uppertitle", "New Flipnotes")
        ugo.set_meta("uppersubbottom", "The most recent flipnotes.")
        flips = Flipnote.objects.all().order_by("-id")[page*50:50]
        selected_newest = "1"
        selected_popular = "0"
        selected_liked = "0"
    ugo.set_meta("uppersubleft", "Flipnotes")
    ugo.set_meta("uppersubright", str(flip_count))
    ugo.add_dropdown({"label": "New Flipnotes", "url": request.build_absolute_uri('/')+"ds/v2-eu/newest.uls", "selected": selected_newest})
    ugo.add_dropdown({"label": "Most Popular", "url": request.build_absolute_uri('/')+"ds/v2-eu/hot.uls", "selected": selected_popular})
    ugo.add_dropdown({"label": "Most Liked", "url": request.build_absolute_uri('/')+"ds/v2-eu/liked.uls", "selected": selected_liked})
    if page != 0:
        ugo.add_item({"label": "Previous", "url": request.build_absolute_uri('/')+"ds/v2-eu/hot.uls?page="+str(page-1)})
    for flip in flips:
        if not flip.channel.show_in_frontpage:
            continue
        if type==None or type==False:
            now = datetime.date.today()
            time_between = now - flip.date
            if int(time_between.days) > 7:
                continue
        if os.path.exists("./files/ppm/"+flip.real_filename+".ppm"):
            with open("./files/ppm/"+flip.real_filename+".ppm", "rb+") as file:
                parser = PPMParser()
                if parser.load(file):
                    ugo.add_item({"url": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+parser.current_filename+".ppm", "file": "./files/ppm/"+parser.current_filename+".ppm", "counter": str(flip.star+flip.green_star+flip.red_star+flip.blue_star+flip.purple_star), "icon": "3"}, False)
                else:
                    continue
        else:
            continue
    if flip_count > (page+1)*50:
        ugo.add_item({"label": "Next", "url": request.build_absolute_uri('/')+"ds/v2-eu/hot.uls?page="+str(page+1)})
    return HttpResponse(ugo.get_ugo())

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
def star(request, reg, file):
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    if "X-Hatena-Star-Count" not in request.headers:
        return HttpResponse(status=403)
    star = int(request.headers["X-Hatena-Star-Count"])
    if star < 1 or star > 65535:
        return HttpResponse(status=403)
    try:
        star_log = StarLog.objects.get(user=session.user, flipnote=flip)
    except ObjectDoesNotExist:
        star_log = StarLog.objects.create(user=session.user, flipnote=flip)
        star_log = StarLog.objects.get(user=session.user, flipnote=flip)
    if request.GET.get("starcolor"):
        user = User.objects.get(id=session.user.id)
        star_type = request.GET.get("starcolor")
        if star_type == "green":
            if star > session.user.green_star:
                return HttpResponse(status=403)
            user.green_star -= star
            star_log.green_star += star
            flip.green_star += star
        elif star_type == "red":
            if star > session.user.red_star:
                return HttpResponse(status=403)
            user.red_star -= star
            star_log.red_star += star
            flip.red_star += star
        elif star_type == "blue":
            if star > session.user.blue_star:
                return HttpResponse(status=403)
            user.blue_star -= star
            star_log.blue_star += star
            flip.blue_star += star
        elif star_type == "purple":
            if star > session.user.purple_star:
                return HttpResponse(status=403)
            user.purple_star -= star
            star_log.purple_star += star
            flip.purple_star += star
        else:
            return HttpResponse(status=403)
        flip.total += star
        user.save()
        star_log.save()
        flip.save()
        return HttpResponse("nice star you got here, can I have it?", content_type="text/plain; charset=utf-16le")
    else:
        if star_log.star >= 10:
            return HttpResponse("nice", content_type="text/plain; charset=utf-16le")
        else:
            if star_log.star + star > 10:
                flip.star += (10 - star_log.star)
                flip.total += (10 - star_log.star)
                flip.save()
                star_log.star = 10
                star_log.save()
                return HttpResponse("hi potential reverse engineer", content_type="text/plain; charset=utf-16le")
            star_log.star += star
            star_log.save()
            flip.star += star
            flip.total += star
            flip.save()
    return HttpResponse("nice", content_type="text/plain; charset=utf-16le")

@csrf_exempt
def flipnote_info(request, reg, file):
    try:
        session = Session.objects.get(token=request.headers['X-DSi-SID'])
    except:
        return HttpResponse(status=403)
    try:
        flip = Flipnote.objects.get(real_filename=file)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    return render(request, "details.html", {"BASE_URI": request.build_absolute_uri('/'),"flipnote": flip, "ppmUri": request.build_absolute_uri('/')+"ds/v2-eu/flipnote/"+file+".ppm", "session": session}, content_type="text/html; charset=utf-8")

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
    if channel.locked:
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
    
@csrf_exempt
def static(request, reg, dir, file):
    if os.path.exists("./ds-static/"+dir+"/"+file):
        with open("./ds-static/"+dir+"/"+file, "rb+") as file:
            return HttpResponse(file.read(), content_type="text/css; charset=utf-8")
    else:
        resp = HttpResponse()
        resp.status_code = 404
        return resp
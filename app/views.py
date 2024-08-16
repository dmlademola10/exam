from django.shortcuts import render, reverse
from django.contrib.auth import hashers
import datetime
from app.models import User, Announcement, ReadArticle
from django.http import HttpResponseRedirect
from django.utils import safestring
from django.contrib import messages
import os
from django.http import HttpResponse
from . import myutils
import html
from django.db.models import Q

# Create your views here.


def signin(req):
    # print("User saved")
    title = "Sign In"
    fields = dict()
    context = dict()
    print("auth", myutils.authenticate_user(req))

    if req.method == "GET":
        if req.GET.get("action") == "signout":
            del req.session["active_user"]
            messages.info(
                req,
                safestring.mark_safe(
                    "<span class='suc'>Signed out successfully!</span>"
                ),
            )

            return HttpResponseRedirect(reverse("signin"))

        if req.GET.get("signed_in") == "true":
            if myutils.authenticate_user(req) is not False:
                context = {
                    "title": title,
                    "func": True,
                }
                return render(req, "signin.html", context=context)
            else:
                return HttpResponseRedirect(reverse("signin"))

    if myutils.authenticate_user(req) is not False:
        return HttpResponseRedirect(reverse("dashboard"))

    if req.method == "POST":
        fields["username"] = req.POST["username"]
        fields["password"] = req.POST["password"]
        fields["close"] = req.POST.get("close", False)
        # fields["relocate"] = req.POST["relocate"]
        if not fields["username"]:
            messages.info(
                req,
                safestring.mark_safe("<span class='err'>Username is empty.</span>"),
            )
            return render(req, "signin.html", {"title": title, "fields": fields})

        if not fields["password"]:
            messages.info(
                req,
                safestring.mark_safe("<span class='err'>Password is empty.</span>"),
            )
            return render(req, "signin.html", {"title": title, "fields": fields})

        if not User.objects.filter(username=fields["username"]).exists():
            messages.info(
                req,
                safestring.mark_safe(
                    "<span class='err'>User does not exist, contact the admins.</span>"
                ),
            )
            return render(req, "signin.html", {"title": title, "fields": fields})

        if (
            hashers.check_password(
                fields["password"],
                User.objects.get(username=fields["username"]).password,
            )
            is not True
        ):
            messages.info(
                req,
                safestring.mark_safe("<span class='err'>Password is incorrect.</span>"),
            )
            return render(req, "signin.html", {"title": title, "fields": fields})

        User.objects.filter(username=fields["username"]).update(
            last_active=datetime.datetime.now()
        )

        req.session["active_user"] = User.objects.get(username=fields["username"]).id
        if fields["close"] == "true":
            return HttpResponseRedirect(reverse("signin") + "?signed_in=true")

        return HttpResponseRedirect(reverse("dashboard"))

        return render(req, "signin.html", {"title": title, "fields": fields})

    if req.GET.get("close", False) == "true":
        fields["close"] = req.GET.get("close", False)

    return render(req, "signin.html", {"title": title, "fields": fields})


def dashboard(req):
    if myutils.authenticate_user(req) is False:
        messages.info(
            req,
            safestring.mark_safe("<span class='err'>You were not signed in.</span>"),
        )
        return HttpResponseRedirect(reverse("signin"))

    title = "Dashboard"
    user = dict()

    if User.objects.get(id=req.session["active_user"]).role != "user":
        title += "(Admin)"
        user["name"] = User.objects.get(id=req.session["active_user"]).name
        user["img"] = User.objects.get(id=req.session["active_user"]).img
        template = "admin/dashboard.html"
        context = {"title": title, "user": user}

    else:
        pass

    return render(req, template, context)


def announcements(req):
    context = dict()
    context["title"] = "Announcements"
    user = dict()
    if myutils.authenticate_user(req) is False:
        messages.info(
            req,
            safestring.mark_safe("<span class='err'>You were not signed in.</span>"),
        )
        return HttpResponseRedirect(reverse("signin"))

    if User.objects.get(id=req.session["active_user"]).role != "user":
        context["title"] += "(Admin)"
        user["name"] = User.objects.get(id=req.session["active_user"]).name
        user["img"] = User.objects.get(id=req.session["active_user"]).img
        context["user"] = user
        context["announcements"] = Announcement.objects.all().order_by("-added_on")
        i = 0
        while i < len(context["announcements"]):
            if not ReadArticle.objects.filter(
                obj_id=context["announcements"][i].id,
                user_id=req.session["active_user"],
            ).exists():
                context["announcements"][i].status = "new"
            i = i + 1

        template = "admin/announcements.html"

    else:
        pass
    return render(req, template, context)


def admins(req):
    context = dict()
    context["title"] = "Announcements"
    user = dict()

    if myutils.authenticate_user(req) is False:
        messages.info(
            req,
            safestring.mark_safe("<span class='err'>You were not signed in.</span>"),
        )
        return HttpResponseRedirect(reverse("signin"))

    if User.objects.get(id=req.session["active_user"]).role != "user":
        context["title"] += "(Admin)"
        user["name"] = User.objects.get(id=req.session["active_user"]).name
        user["img"] = User.objects.get(id=req.session["active_user"]).img
        context["user"] = user
        context["admins"] = User.objects.filter(~Q(role="user")).order_by(
            "-date_joined"
        )
        template = "admin/admins.html"

    else:
        pass
    return render(req, template, context)

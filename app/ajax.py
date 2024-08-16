from . import myutils
from django.utils import safestring
from app.models import User, Announcement, ReadArticle, User
from django.http import HttpResponse
import json
import html
from django.shortcuts import reverse
import datetime
from django.db.models import Q
from django.core import validators, exceptions


def get_announcement(req, id):
    context = dict()
    context["success"] = False

    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if req.method == "GET":
        if Announcement.objects.filter(id=int(id)).exists():
            announcement = Announcement.objects.get(id=int(id))
            context["message"] = dict()
            context["message"]["title"] = announcement.title
            context["message"]["details"] = announcement.details

            if announcement.announcer == req.session["active_user"]:
                context["message"]["announcer"] = "You"

            else:
                context["message"]["announcer"] = User.objects.get(
                    id=announcement.announcer
                ).name

            context["message"]["datetime"] = announcement.added_on.strftime(
                "%A, %B %d, %Y at %I:%M%p"
            )

            if not ReadArticle.objects.filter(
                obj_id=int(id), user_id=req.session["active_user"]
            ).exists():
                ReadArticle(obj_id=int(id), user_id=req.session["active_user"]).save()

            if req.GET.get("edit", False) is not False:
                context["message"]["id"] = str(announcement.id)
                context["message"]["title"] = html.unescape(context["message"]["title"])
                context["message"]["details"] = html.unescape(
                    context["message"]["details"].replace("<br />", "\n")
                )
                del context["message"]["announcer"]
                del context["message"]["datetime"]

            context["success"] = True
            context["message"] = json.dumps(context["message"])

        else:
            context["message"] = "Sorry, that announcement doesn't exist."

    else:
        context["message"] = "Sorry, an error occurred."

    return HttpResponse(content=json.dumps(context))


def add_announcement(req):
    context = dict()
    fields = dict()
    context["success"] = False
    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if (
        req.method == "POST"
        and User.objects.get(id=req.session["active_user"]).role != "user"
    ):
        fields["title"] = myutils.trim(req.POST["new_title"])
        fields["details"] = myutils.trim(req.POST["new_details"])

        if not fields["title"]:
            context["message"] = "Title can't be empty."
            return HttpResponse(content=json.dumps(context))

        if not fields["details"]:
            context["message"] = "Details can't be empty."
            return HttpResponse(content=json.dumps(context))

        if Announcement.objects.filter(
            title=html.escape(fields["title"]),
            details=html.escape(fields["details"]).replace("\n", "<br />"),
        ).exists():
            context[
                "message"
            ] = "Announcement with same title and details already exists."
            return HttpResponse(content=json.dumps(context))

        if len(fields["title"]) < 3:
            context["message"] = "Title can't have less than 3 characters."
            return HttpResponse(content=json.dumps(context))

        if len(fields["title"]) > 30:
            context["message"] = "Title can't have more than 30 characters."
            return HttpResponse(content=json.dumps(context))

        if len(fields["details"]) < 15:
            context["message"] = "Details can't have less than 15 characters."
            return HttpResponse(content=json.dumps(context))

        if len(fields["details"]) > 500:
            context["message"] = "Details can't have more than 500 characters."
            return HttpResponse(content=json.dumps(context))

        Announcement(
            announcer=req.session["active_user"],
            title=myutils.trim(html.escape(req.POST["new_title"])),
            details=myutils.trim(
                html.escape(req.POST["new_details"]).replace("\n", "<br />")
            ),
        ).save()
        ReadArticle(
            obj_id=Announcement.objects.get(
                announcer=req.session["active_user"],
                title=myutils.trim(html.escape(req.POST["new_title"])),
                details=myutils.trim(
                    html.escape(req.POST["new_details"]).replace("\n", "<br />")
                ),
            ).id,
            user_id=req.session["active_user"],
        ).save()

        context["success"] = True
        context["message"] = "Saved successfully."

    else:
        context["message"] = "Sorry, an error occurred."

    return HttpResponse(json.dumps(context))


def refresh_announcements(req):
    context = dict()
    user = dict()
    context["success"] = False
    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if req.method == "GET":
        i = 0
        context["announcements"] = Announcement.objects.all().order_by("-added_on")
        while i < len(context["announcements"]):
            if not ReadArticle.objects.filter(
                obj_id=context["announcements"][i].id,
                user_id=req.session["active_user"],
            ).exists():
                context["announcements"][i].status = "new"
            else:
                context["announcements"][i].status = ""

            i = i + 1

        context["success"] = True
        context["message"] = myutils.format_announcements(context["announcements"])
        del context["announcements"]

    else:
        context["message"] = "Sorry, an error occurred."

    return HttpResponse(content=json.dumps(context))


def delete_announcement(req, id):
    context = dict()
    context["success"] = False
    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if Announcement.objects.filter(id=int(id)).exists():
        Announcement.objects.get(id=int(id)).delete()

        ReadArticle.objects.filter(obj_id=int(id)).delete()

        context["success"] = True
        context["message"] = "Deleted successfully."

    else:
        context["message"] = "Sorry, that announcement doesn't exist."

    return HttpResponse(content=json.dumps(context))


def edit_announcement(req):
    context = dict()
    fields = dict()
    context["success"] = False

    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if (
        req.method == "POST"
        and User.objects.get(id=req.session["active_user"]).role != "user"
    ):
        fields["id"] = myutils.trim(req.POST["edit_id"])
        fields["title"] = myutils.trim(req.POST["edit_title"])
        fields["details"] = myutils.trim(req.POST["edit_details"])

        if not fields["id"] or not fields["id"].isnumeric():
            context["message"] = "Sorry, an error occurred, try refreshing the page."
            return HttpResponse(content=json.dumps(context))

        if not fields["title"]:
            context["message"] = "Title can't be empty."
            return HttpResponse(content=json.dumps(context))

        if not fields["details"]:
            context["message"] = "Details can't be empty."
            return HttpResponse(content=json.dumps(context))

        if Announcement.objects.filter(
            Q(title=html.escape(fields["title"]))
            & Q(details=html.escape(fields["details"])),
            ~Q(id=fields["id"]),
        ).exists():
            context[
                "message"
            ] = "Another announcement with same title and details already exists."
            return HttpResponse(content=json.dumps(context))

        if len(fields["title"]) < 3:
            context["message"] = "Title can't have less than 3 characters."
            return HttpResponse(content=json.dumps(context))

        if len(fields["title"]) > 30:
            context["message"] = "Title can't have more than 30 characters."
            return HttpResponse(content=json.dumps(context))

        if len(fields["details"].replace("<br />", " ")) < 15:
            context["message"] = "Details can't have less than 15 characters."
            return HttpResponse(content=json.dumps(context))

        if len(fields["details"].replace("<br />", " ")) > 500:
            context["message"] = "Details can't have more than 500 characters."
            return HttpResponse(content=json.dumps(context))

        Announcement.objects.filter(id=fields["id"]).update(
            title=myutils.trim(html.escape(req.POST["edit_title"])),
            details=myutils.trim(
                html.escape(req.POST["edit_details"]).replace("\n", "<br />")
            ),
            added_on=datetime.datetime.now(),
        )
        ReadArticle.objects.filter(obj_id=fields["id"]).delete()
        ReadArticle(
            obj_id=fields["id"],
            user_id=req.session["active_user"],
        ).save()

        context["success"] = True
        context["message"] = "Saved successfully."

    else:
        context["message"] = "Sorry, an error occurred."

    return HttpResponse(json.dumps(context))


def add_admin(req):
    context = dict()
    fields = dict()
    context["success"] = False
    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if (
        req.method == "POST"
        and User.objects.get(id=req.session["active_user"]).role == "s"
    ):

        user = myutils.Person(
            myutils.trim(req.POST["new_fullname"]),
            myutils.trim(req.POST["new_email"]),
            myutils.trim(req.POST["new_role"]),
            myutils.trim(req.POST["access"]),
        )
        if not user.fullname:
            context["message"] = "Fullname is required."
            return HttpResponse(content=json.dumps(context))

        if len(user.fullname) < 3:
            context["message"] = "Fullname must have more than three characters."
            return HttpResponse(content=json.dumps(context))

        if len(user.fullname) > 20:
            context["message"] = "Fullname must not have more than twenty characters."
            return HttpResponse(content=json.dumps(context))

        if not user.email:
            context["message"] = "Email is required."
            return HttpResponse(content=json.dumps(context))

        try:
            validators.validate_email(user.email)
        except exceptions.ValidationError:
            context["message"] = "Email is invalid."
            return HttpResponse(content=json.dumps(context))

        if not user.role or user.role not in ["s", "a"]:
            context["message"] = "An error occurred, try refreshing the page."
            return HttpResponse(content=json.dumps(context))

        if not user.access or user.access not in ["true", "false"]:
            context["message"] = "An error occurred, try refreshing the page."
            return HttpResponse(content=json.dumps(context))

        User(
            name=user.escape()["fullname"],
            suspended=True if user.access == "true" else False,
            reason="User wasn't given immediate access."
            if user.access == "true"
            else "",
            email=user.escape()["email"],
            role=user.escape()["role"],
        ).save()

        context["success"] = True
        context["message"] = safestring.mark_safe("Successfully added new admin.")
        return HttpResponse(content=json.dumps(context))

    else:
        context["message"] = safestring.mark_safe(
            "An error occurred, You can't add this user."
        )
        return HttpResponse(content=json.dumps(context))


def get_admin(req, id):
    context = dict()
    context["success"] = False

    if myutils.authenticate_user(req) is False:
        context["message"] = safestring.mark_safe(
            "You are not signed in. <a href='"
            + reverse("signin")
            + "?close=true"
            + "' target='_blank'>Click to sign in.</a>"
        )
        return HttpResponse(content=json.dumps(context))

    if req.method == "GET":
        if User.objects.filter(id=int(id), role="s" | "a").exists():
            admin = User.objects.get(id=int(id))
            context["message"] = dict()
            context["message"]["title"] = announcement.title
            context["message"]["details"] = announcement.details

            if announcement.announcer == req.session["active_user"]:
                context["message"]["announcer"] = "You"

            else:
                context["message"]["announcer"] = User.objects.get(
                    id=announcement.announcer
                ).name

            context["message"]["datetime"] = announcement.added_on.strftime(
                "%A, %B %d, %Y at %I:%M%p"
            )

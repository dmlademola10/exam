from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.


def initial(req):
    return HttpResponseRedirect(redirect_to="exam/")

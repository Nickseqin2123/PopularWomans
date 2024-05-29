from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def login_user(request: HttpRequest):
    return HttpResponse('login')


def logout_user(request: HttpRequest):
    return HttpResponse('logout')
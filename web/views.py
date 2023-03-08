from django.http import HttpResponse
from django.shortcuts import render


def main_view(request):
    return HttpResponse('<h1> Привет мир </h1>')
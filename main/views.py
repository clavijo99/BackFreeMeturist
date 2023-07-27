from django.shortcuts import render
from django.http import HttpResponse

def home(request): return HttpResponse('<h1 style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; align-content: center;" > It worked...</h1>')

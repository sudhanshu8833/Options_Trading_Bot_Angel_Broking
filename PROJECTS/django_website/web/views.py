from django.shortcuts import render
from django.shortcuts import render, redirect
# Create your views here.

def index(request):
    return render(request,'web/index.html')
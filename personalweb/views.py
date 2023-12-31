from django.shortcuts import render,redirect

def home(request):
    return render(request,"index.html")


def resume(request):
    return render(request,'resume.html')
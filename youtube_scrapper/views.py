from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from . import functions

@csrf_exempt
def scrap(request):
    if request.method=="POST":
        link=request.POST.get('link')
        data=[]
        functions.get_data(link,data)
        return render(request,"youtube_scrap.html",{"data":data,})
    return render(request,"youtube_scrap.html",{"data":[[]]})

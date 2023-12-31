from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt

from . import models,forms
import random
@csrf_exempt
def random_text():
    text="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*=+?.;:"
    id=""
    for i in range(6):
        id=id+random.choice(text)
    return id
@csrf_exempt
def shortener(request):
    if request.method=="POST":
        form=forms.link_form(request.POST)
        if form.is_valid():
            link=form.cleaned_data['link']
            if models.link_db.objects.filter(link=link).exists():
                db=models.link_db.objects.get(link=link)
                return render(request,"link.html",{"form":forms.link_form,"shorten":"https://rahim-khan.azurewebsites.net/shortener/s/"+db.link_id,"original":link})
            random_txt=random_text()
            while models.link_db.objects.filter(link_id=random_txt):
                random_txt=random_text()
            p=models.link_db(link=link,link_id=random_txt)
            p.save()
            return render(request,"link.html",{"form":forms.link_form,"shorten":"https://rahim-khan.azurewebsites.net/shortener/s/"+random_txt,"original":link})
        return HttpResponse("thanks")
    return render(request,'link.html',{"form":forms.link_form})

@csrf_exempt
def urlRedirect(request,slug):
    if models.link_db.objects.filter(link_id=slug).exists():
        data=models.link_db.objects.get(link_id=slug)
        # print(data.link)
        link=data.link
        return redirect(link)
    return render(request,"broken_link.html")
from django.shortcuts import render
from .utils import predict
import pandas as pd
import os
import json
# Create your views here.
# def stock(request):
#     return render(request,"stocks.html")

def stock(request):
    if request.method=="POST":
        company=request.POST.get('company')
        select=request.POST.get("select")
        key=company.split("(")[0]
        key=key.strip()
        obj=predict(key,select)
        test,pred,next=obj.make_prediction()
        df=pd.read_csv(os.path.join("artifacts",'stocks.csv'))
        labels=list(df['Unnamed: 0'])[70:]
        data=json.dumps({"pred":pred,"labels":labels,"actual":test})
        return render(request,'stocks.html',{"arr":data,"next":next[0],"company":company})
    return render(request,"stocks.html",{"arr":{"pred":[],"labels":[],"actual":[]}})


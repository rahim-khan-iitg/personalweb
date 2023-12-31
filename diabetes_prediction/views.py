from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import pickle
import warnings 
warnings.filterwarnings("ignore")
@csrf_exempt
def predict(request):
    scaler=pickle.load(open('media/diabetes_model/scaler.pkl','rb'))
    model=pickle.load(open('media/diabetes_model/model.pkl','rb'))
    if request.method=="POST":
        pregs=float(request.POST.get('pregs'))
        glucose=float(request.POST.get('glucose'))
        b_pressure=float(request.POST.get('b-pressure'))
        s_thickness=float(request.POST.get("s-thickness"))
        insulin=float(request.POST.get('insulin'))
        bmi=float(request.POST.get('bmi'))
        dpf=float(request.POST.get('dpf'))
        age=float(request.POST.get('age'))
        sample=np.array([[pregs,glucose,b_pressure,s_thickness,insulin,bmi,dpf,age]])
        sample=scaler.transform(sample)
        prediction=model.predict(sample)
        result=""
        if prediction[0]==0:
            result="No Diabetes"
        else:
            result="Diabetes"
        return render(request,"diabetes.html",{"prediction":result})
    return render(request,"diabetes.html")
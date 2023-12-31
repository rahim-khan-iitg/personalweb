from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pandas
import pickle

@csrf_exempt
def email_classifier(request):
    if request.method=="POST":
        model=pickle.load(open('media/email_model/model.pkl','rb'))
        vectorizer=pickle.load(open("media/email_model/vectorizer.pkl",'rb'))
        text=request.POST.get('textarea')
        text=text.strip()
        email=vectorizer.transform(pandas.DataFrame([text],columns=['Text']).Text)
        result=model.predict(email)
        prediction="Spam"
        if result[0]==0:
            prediction="Not Spam"
        return render(request,'email_classifier.html',{"prediction":prediction})

    return render(request,'email_classifier.html')

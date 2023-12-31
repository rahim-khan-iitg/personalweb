from  django import forms

class link_form(forms.Form):
    link=forms.CharField(max_length=1000,required=True)
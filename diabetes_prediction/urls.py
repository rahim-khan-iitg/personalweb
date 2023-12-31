from django.urls import path
from . import views

urlpatterns=[
    path("",views.predict,name='perd_diabetes'),
]
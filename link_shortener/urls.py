from django.urls import path
from . import views

urlpatterns=[
    path("",views.shortener,name="shortener"),
    path("s/<str:slug>",views.urlRedirect,name="redirect")
]
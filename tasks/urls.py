from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('newtask', views.newtask, name='newtask'),
    path('getcaptcha', views.getcaptcha, name='getcaptcha'),
]
from django.urls import path

from .views import taskNew, login, session, taskList

urlpatterns = [
    path('login', login.login, name='login'),
    path('newtask', taskNew.newtask, name='newtask'),
    path('getcaptcha', login.getcaptcha, name='getcaptcha'),
    path('refreshcaptcha', login.refreshcaptcha, name='refreshcaptcha'),
    path('isLogin', login.isLogin, name='isLogin'),
    path('tasklist', taskList.tasklist, name='tasklist'),
]

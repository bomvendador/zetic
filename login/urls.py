from django.urls import path
# import views as pdf_views
from login import views as login_views

urlpatterns = [
    path('', login_views.home, name="login_home"),
    path('login', login_views.login, name="login_login"),

]
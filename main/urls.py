from django.urls import path

from main import views 

app_name = 'main'

urlpatterns = [
    path("", views.LoginView.as_view(), name='login'), 
    path("logout/", views.logout, name='logout'),
    path("user/create/", views.RegisterUserView.as_view(), name='create_user'), 
]

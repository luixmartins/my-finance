from django.urls import path

from main import views 

app_name = 'main'

urlpatterns = [
    path("", views.Home.as_view(), name='home'), 
    path("user/create/", views.RegisterUserView.as_view(), name='create_user'), 
]

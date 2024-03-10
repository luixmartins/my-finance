from django.urls import path

from finance import views 

app_name = 'finance'

urlpatterns = [
    path("", views.HomeView.as_view(), name='home')
]

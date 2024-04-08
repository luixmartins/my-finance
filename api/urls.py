from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls')), 
    path('finance/', include('finance.urls')), 
]

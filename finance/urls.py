from django.urls import path 

from finance.views import CategoryCreateView

urlpatterns = [
    path('categories/', CategoryCreateView.as_view(), name='create-list-category')
]

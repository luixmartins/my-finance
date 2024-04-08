from django.urls import path 

from finance.views import CategoryListCreateView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='create-list-category')
]

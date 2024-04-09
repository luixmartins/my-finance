from django.urls import path 

from finance.views import CategoryListCreateView, CategoryDeleteView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='create-list-category'), 
    path('categories/<int:pk>/', CategoryDeleteView.as_view(), name='delete-category')
]

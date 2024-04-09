from django.urls import path 

from finance.views import CategoryListCreateView, CategoryDeleteView, SpentListCreateView, SpentDetailView

urlpatterns = [
    #categories 
    path('categories/', CategoryListCreateView.as_view(), name='create-list-category'), 
    path('categories/<int:pk>/', CategoryDeleteView.as_view(), name='delete-category'), 

    #spents 
    path('spents/', SpentListCreateView.as_view(), name='create-list-spent'), 
    path('spents/<int:pk>/', SpentDetailView.as_view(), name='detail-spent'), 
    
]

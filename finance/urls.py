from django.urls import path 

from finance.views import CategoryListCreateView, CategoryDetailView, SpentListCreateView

urlpatterns = [
    #categories 
    path('categories/', CategoryListCreateView.as_view(), name='create-list-category'), 
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='detail-category'), 

    # #spents 
    path('spents/', SpentListCreateView.as_view(), name='list-create-spent'), 
    # path('spents/<int:pk>/', SpentDetailView.as_view(), name='detail-spent'), 
    
    # #recurring_spents
    # path('spents/recurring/', RecurringSpentListCreateView.as_view(), name='create-list-recurring'), 
    # path('spents/recurring/<int:pk>/', RecurringSpentDetailView.as_view(), name='detail-recurring-spent')
]
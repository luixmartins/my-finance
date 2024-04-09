from django_filters import rest_framework as filters 

from finance.models import SpentModel 

class SpentModelFilter(filters.FilterSet): 
    month = filters.NumberFilter(field_name='date', lookup_expr='month')
    year = filters.NumberFilter(field_name='date', lookup_expr='year')

    class Meta: 
        model = SpentModel 
        fields = ['month', 'year']
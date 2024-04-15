from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend

from finance.serializers import CategorySerializer, SpentSerializer
from finance.models import CategoryModel, SpentModel
from finance.filters import SpentModelFilter
from finance.utils import update_recurring_spents

class CategoryListCreateView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request): 
        categories = CategoryModel.objects.filter(user=request.user)
        
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)
        
    
    def post(self, request): 
        serializer = CategorySerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid(): 
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
                                                                                                                                                              
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryModel.objects.filter(user=self.request.user)

class SpentListCreateView(APIView): 
    permission_classes = [IsAuthenticated]
    filterset_class = SpentModelFilter

    def get(self, request): 
        user=request.user 
        spents = SpentModel.objects.filter(user=user)
        
        update_recurring_spents(user=user, spents=spents)

        filter_backend = DjangoFilterBackend()
        filtered_spents = filter_backend.filter_queryset(request, spents, self)

        serializer = SpentSerializer(filtered_spents, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request): 
        serializer = SpentSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid(): 
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
                                                                                                                                                              
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# class SpentListCreateView(APIView): 
#     permission_classes = [IsAuthenticated]
#     filterset_class = SpentModelFilter

#     def get(self, request): 
#         recurring_spents = RecurringSpentModel.objects.filter(spent__member=request.user)
#         for spent in recurring_spents: 
#             spent.update_last_billing_date

#             spent.save()

#             print(type(spent))
#         spents = SpentModel.objects.filter(member=request.user)

#         filter_backend = DjangoFilterBackend()
#         filtered_spents = filter_backend.filter_queryset(request, spents, self)

#         serializer = SpentSerializer(filtered_spents, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request): 
#         serializer = SpentSerializer(data=request.data, context={'user': request.user})

#         if serializer.is_valid(): 
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
# class SpentDetailView(generics.RetrieveUpdateDestroyAPIView): 
#     permission_classes = [IsAuthenticated]
#     serializer_class = SpentSerializer

#     def get_queryset(self):
#         return SpentModel.objects.filter(member=self.request.user)
    
#     def update(self, request, *args, **kwargs): 
#         instance = self.get_object()
#         serializer = SpentSerializer(instance, data=request.data, partial=True, context={'user': request.user})

#         if serializer.is_valid(): 
#             serializer.save() 

#             return Response(serializer.data)
#         return Response(serializer.errors)
    
# class RecurringSpentListCreateView(APIView): 
#     permission_classes = [IsAuthenticated]

#     def get(self, request): 
#         spents = RecurringSpentModel.objects.filter(spent__member=request.user)
#         serializer = RecurringSpentSerializer(spents, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request): 
#         context = { 
#             'user': request.user, 
#             'data': request.data['spent']
#         }

#         serializer = RecurringSpentSerializer(data=request.data, context=context)

#         if serializer.is_valid(): 
#             serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RecurringSpentDetailView(generics.RetrieveUpdateDestroyAPIView): 
#     permission_classes = [IsAuthenticated]
#     serializer_class = RecurringSpentSerializer

#     def get_queryset(self): 
#         return RecurringSpentModel.objects.filter(spent__member=self.request.user)
    
#     def update(self, request, *args, **kwargs): 
#         instance = self.get_object()

#         serializer = RecurringSpentSerializer(instance, data=request.data, partial=True, context={'user': request.user})

#         if serializer.is_valid(): 
#             test = serializer.save() 
#             print(test)

#             return Response(serializer.data)
        
#         return Response(serializer.errors)
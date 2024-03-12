from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class CategoryModel(models.Model): 
    '''
        Table category. 
        
        - stores category data with unique names. 
    '''
    name = models.CharField(max_length=100, verbose_name = 'Category name', unique = True)

    class Meta: 
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class MemberCategoryModel(models.Model): 
    '''
        Relationship table for user and category.

        - The business rule determines that each user can create and maintain a category. 
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'user id')
    category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name = 'category id')

    class Meta: 
        db_table = 'member_category'
        


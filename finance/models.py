from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError

from datetime import date 

def validate_category(name): 
    if len(name) < 2: 
        raise ValidationError('Text size is too short. Enter a valid text.')
    if name[0].isdigit(): 
        raise ValidationError('The first letter cannot be a number. Enter a valid text.')
    
    return name.lower()

def validate_value_spent(value): 
    if not isinstance(value, (int, float)): 
        raise ValidationError('The value must be an int or float instance.')
    
    if value <= 0: 
        raise ValidationError('The value must be greater than zero.')

class CategoryModel(models.Model): 
    name = models.CharField(max_length=255, unique=True, validators=[validate_category])

    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name 
    
class MemberCategoryModel(models.Model): 
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='category')

    class Meta: 
        verbose_name = 'Member and Category'
        verbose_name_plural = 'Members and Categories'
        unique_together = [['member', 'category']]

    def __str__(self) -> str:
        return f'{self.member.username} - {self.category.name}'

class SpentModel(models.Model): 
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_value_spent])
    date = models.DateField(default=date.today, blank=True)
    member_category = models.ForeignKey(MemberCategoryModel, on_delete=models.CASCADE, related_name='member_category')

    def __str__(self) -> str:
        return f'{self.date} - {self.value}'
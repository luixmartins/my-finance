from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.db.models import Q

from datetime import date, timedelta

def validate_category(name): 
    if len(name) < 2: 
        raise ValidationError('Text size is too short. Enter a valid text.')
    if name[0].isdigit(): 
        raise ValidationError('The first letter cannot be a number. Enter a valid text.')
    
    return name.lower()

def validate_positive_values(value): 
    if not isinstance(value, (int, float)): 
        raise ValidationError('The value must be an int or float instance.')
    
    if value <= 0: 
        raise ValidationError('The value must be greater than zero.')
    
class CategoryModel(models.Model): 
    name = models.CharField(max_length=255, validators=[validate_category])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["name"]
        unique_together = [['user', 'name']]

    def __str__(self) -> str:
        return f'{self.user.username} - {self.name}'   

class SpentModel(models.Model): 
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_values])
    date = models.DateField(default=date.today, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateField(auto_now=True, blank=True)
    recurring = models.BooleanField(default=False)
    period = models.IntegerField(null=True, blank=True, validators=[validate_positive_values])

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_spent')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='category_spent')

    def create_new_spent_for_recurring(self): 
        if self.recurring is True: 
            new_date = self.date + timedelta(days=self.period)

            if not SpentModel.objects.filter(Q(date=new_date, description=self.description, period=self.period)).exists() and new_date <= date.today():  
                        SpentModel.objects.create(
                            description = self.description, 
                            value = self.value, 
                            date = new_date, 
                            recurring = True, 
                            period = self.period, 
                            user=self.user, 
                            category=self.category, 
                        )

    def __str__(self) -> str:
        return f'{self.date} - {self.value}'
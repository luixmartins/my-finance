from typing import Iterable
from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError

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
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive_values])
    date = models.DateField(default=date.today, blank=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member_spent')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='category_spent')

    def save(self, *args, **kwargs):
        try: 
            MemberCategoryModel.objects.get(category=self.category)
        except: 
            raise ValidationError('The category does not exist for this user.')

        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f'{self.date} - {self.value}'
    
class RecurringSpentModel(models.Model): 
    period = models.IntegerField(validators=[validate_positive_values])
    last_billing_date = models.DateField(default=date.today, blank=True)
    spent = models.ForeignKey(SpentModel, on_delete=models.CASCADE, related_name='spent')

    @property
    def next_billing_date(self):
        return self.last_billing_date + timedelta(days=self.period)

    def update_last_billing_date(self): 
        if date.today() >= self.next_billing_date: 
            self.last_billing_date = self.next_billing_date 

            self.save()

    class Meta: 
        verbose_name = 'Recurring Spent'
        verbose_name_plural = 'Recurring Spent'
        ordering = ['-last_billing_date']

#recurring_spents = RecurringSpentModel.objects.filter(spent__member=member)
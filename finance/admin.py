from django.contrib import admin

from finance import models 

# Register your models here.
admin.site.register(models.CategoryModel)
admin.site.register(models.MemberCategoryModel)
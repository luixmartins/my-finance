from django.contrib import admin

from finance import models 

admin.site.register(models.CategoryModel)
admin.site.register(models.SpentModel)

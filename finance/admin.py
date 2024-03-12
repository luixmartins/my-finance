from django.contrib import admin

from finance.models import CategoryModel, MemberCategoryModel
# Register your models here.
@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin): 
    pass 

@admin.register(MemberCategoryModel)
class MemberCategoryAdmin(admin.ModelAdmin): 
    pass 
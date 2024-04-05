# Generated by Django 5.0.3 on 2024-04-04 23:58

import datetime
import django.db.models.deletion
import finance.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, validators=[finance.models.validate_category])),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SpentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, validators=[finance.models.validate_value_spent])),
                ('date', models.DateField(blank=True, default=datetime.date.today)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_spent', to='finance.categorymodel')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_spent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MemberCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='finance.categorymodel')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Member and Category',
                'verbose_name_plural': 'Members and Categories',
                'unique_together': {('member', 'category')},
            },
        ),
    ]

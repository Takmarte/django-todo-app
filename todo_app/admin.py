from django.contrib import admin
from .models import Todos, Category
# Register your models here.

admin.site.register(Todos)
admin.site.register(Category)
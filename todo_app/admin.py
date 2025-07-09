from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from unfold.admin import ModelAdmin
from .models import Todos, Category
# Register your models here.

@admin.register(Todos)
class TodosAdmin(ModelAdmin):
    list_display = ("title", "user", "is_private", "finished", "date")
    list_filter = ("is_private", "finished", "user", "category")
    search_fields = ("title", "user", "description")

    
class TodoInline(admin.TabularInline):
    model = Todos
    fields = ('linked_title', 'finished', 'deadline', 'user')
    readonly_fields = ('linked_title', 'finished', 'deadline', 'user')
    extra = 0
    can_delete = False
    verbose_name_plural = "Related To-Dos"
    
    def linked_title(self, obj):
        if obj.id:
            url = reverse('admin:todo_app_todos_change', args=[obj.id])
            return format_html('<a href="{}">{}</a>', url, obj.title)
        return "-"
    linked_title.short_description = "Title"

class SubCategoryInline(admin.TabularInline):
    model = Category
    fk_name = 'parent'
    fields = ('linked_name',)
    readonly_fields = ('linked_name',)
    extra = 0
    verbose_name_plural = "Subcategories"
    
    def linked_name(self, obj):
        url = reverse("admin:todo_app_category_change", args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.name)
    linked_name.short_description = "Subcategory"    
    
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "show_subcategories")
    search_fields = ("name",)
    ordering = ("parent__name", "name")
    inlines = [SubCategoryInline, TodoInline]

    def show_subcategories(self, obj):
        return ", ".join([child.name for child in obj.subcategories.all()]) or "-"
    show_subcategories.short_description = "Subcategories"
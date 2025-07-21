
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from unfold.admin import ModelAdmin
from .models import Category, DailyTodoList, Todos, TodoItem

class TodoItemInline(admin.TabularInline):
    model = TodoItem
    extra = 1
    fields = ('text', 'done')
    show_change_link = True

class TodoInline(admin.TabularInline):
    model = Todos
    extra = 0
    fields = ('title', 'finished', 'is_private', 'deadline')
    show_change_link = True

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
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('name',)
    inlines = [SubCategoryInline]

@admin.register(DailyTodoList)
class DailyTodoListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date', 'category')
    list_filter = ('date', 'user', 'category')
    search_fields = ('name', 'user__username')
    inlines = [TodoInline]
    ordering = ('-date',)

@admin.register(Todos)
class TodosAdmin(ModelAdmin):
    list_display = ('title', 'daily_list', 'finished', 'is_private', 'deadline', 'date_created', 'finished_date')
    search_fields = ('title', 'description')
    list_filter = ('finished', 'is_private', 'deadline', 'daily_list__user')
    date_hierarchy = 'date_created'
    inlines = [TodoItemInline]
    ordering = ('-date_created',)

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'todo', 'done')
    list_filter = ('done', 'todo')
    search_fields = ('text',)
    ordering = ('todo',)

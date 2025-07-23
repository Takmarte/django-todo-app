from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, DailyTodoList, Todos, TodoItem


class DailyTodoInline(TabularInline):
    model = DailyTodoList
    extra = 0
    tab = True
    show_change_link = True
    fields = ('name','date','user')

class TodoItemInline(TabularInline):
    model = TodoItem
    extra = 1
    tab = True
    show_change_link = True
    fields = ('text', 'done')


class TodoInline(TabularInline):
    model = Todos
    extra = 0
    tab = True
    show_change_link = True
    fields = ('title', 'finished', 'is_private', 'deadline')


class SubCategoryInline(TabularInline):
    model = Category
    fk_name = 'parent'
    extra = 0
    fields = ('linked_name',)
    readonly_fields = ('linked_name',)
    tab = True

    def linked_name(self, obj):
        url = reverse("admin:todo_app_category_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.name)
    linked_name.short_description = "Subcategories"




class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'parent', 'subcategories_count')
    search_fields = ('name',)
    list_filter = ('parent',)
    ordering = ('name',)
    inlines = [SubCategoryInline,DailyTodoInline]
    fieldsets = (
        (_("Category details"), {
            'fields': ('name', 'parent'),
            'classes': ['tab'],
        }),
    )

    def subcategories_count(self, obj):
        return obj.subcategories.count()
    subcategories_count.short_description = "Subcategories"


class DailyTodoListAdmin(ModelAdmin):
    list_display = ('name', 'user', 'date', 'category_name', 'todos_count')
    search_fields = ('name', 'user__username')
    list_filter = ('date', 'user', 'category')
    ordering = ('-date',)
    date_hierarchy = 'date'
    inlines = [TodoInline]
    fieldsets = (
        (_("List Overview"), {
            'fields': ('name', 'date', 'user', 'category'),
            'classes': ['tab'],
        }),
    )

    def todos_count(self, obj):
        return obj.todos.count()
    todos_count.short_description = "Todos"

    def category_name(self, obj):
        return obj.category.name if obj.category else "-"
    category_name.short_description = "Category"


class TodosAdmin(ModelAdmin):
    list_display = (
        'title', 'daily_list', 'user', 'is_private', 'finished', 'deadline', 'finished_date', 'subtask_count', 'progress', 
    )
    search_fields = ('title', 'description', 'daily_list__name', 'user__username')
    list_filter = ('finished', 'is_private', 'deadline', 'daily_list__user')
    ordering = ('-date_created',)
    readonly_fields = ('date_created', 'finished_date', 'progress')
    inlines = [TodoItemInline]
    fieldsets = (
        (_("Basic Info"), {
            "fields": ("title", "description", "daily_list", "user", "is_private"),
            "classes": ["tab"],
        }),
        (_("Status & Timing"), {
            "fields": ("finished", "deadline", "date_created", "finished_date", "progress"),
            "classes": ["tab"],
        }),
    )
    def get_category(self,obj):
        return obj.daily_list.category if obj.daily_list and obj.daily_list.category else "-"
    get_category.short_description = "Category"

    def subtask_count(self, obj):
        return obj.items.count()
    subtask_count.short_description = "Subtasks"


class TodoItemAdmin(ModelAdmin):
    list_display = ('text', 'todo', 'done')
    search_fields = ('text', 'todo__title')
    list_filter = ('done',)
    ordering = ('todo',)
    fieldsets = (
        (_("Subtask Detail"), {
            'fields': ('text', 'done', 'todo'),
            'classes': ['tab'],
        }),
    )


# ================== REGISTER ==========================

from django.contrib import admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(DailyTodoList, DailyTodoListAdmin)
admin.site.register(Todos, TodosAdmin)


from django import forms
from .models import Todos, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models

class ListForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ["title", "description", "finished", "date", "deadline", "category", "is_private"]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_private'}),
        }

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['category'].queryset = Category.objects.all().order_by('parent__name', 'name')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','parent']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
            

from django import forms
from .models import Todos, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models

class ListForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ["title", "description", "finished", "date", "deadline", "category", "is_private"]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['is_private'].widget.attrs.update({'class': 'form-check-input'})

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

from django import forms
from .models import Todos, TodoItem, DailyTodoList, Category

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todos
        fields = ["title", "description", "finished", "deadline", "is_private"]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_private'}),
            'finished': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_finished'}),
        }

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['text', 'done']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DailyTodoListForm(forms.ModelForm):
    class Meta:
        model = DailyTodoList
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
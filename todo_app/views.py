from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Todos, Category
from .forms import ListForm , CategoryForm
from datetime import datetime

# Create your views here.

@login_required
def todo(request):
    todo_list = Todos.objects.all()
    categories = Category.objects.all()
    return render(request, "todo_app/todo.html", {
        'todo_list': todo_list,
        'categories': categories
    })
    
@login_required
def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            todo_list = Todos.objects.all()
        else:
            todo_list = Todos.objects.filter(user=request.user)
    else:
        todo_list = []  

    categories = Category.objects.all()
    return render(request, "todo_app/index.html", {
        'todo_list': todo_list,
        'categories': categories
    })


def about(request):
    return render(request,"todo_app/about.html")

@login_required
def create(request):  
    if request.method == "POST":  
        form = ListForm(request.POST)  
        if form.is_valid():  
            todo = form.save(commit=False)  
            todo.user = request.user  
            if todo.finished:  
                todo.finished_date = datetime.now()  
            todo.save()  
            return redirect("index")  
    else:  
        form = ListForm()  

    return render(request, "todo_app/create.html", {'form': form})



@login_required
def delete(request, Todos_id):
    todo = get_object_or_404(Todos, pk=Todos_id)
    category_id = todo.category.id if todo.category else None
    todo.delete()

    if category_id:
        return redirect('category_view', category_id=category_id)
    else:
        return redirect("index")


@login_required
def yes_finish(request,Todos_id):
    todo = Todos.objects.get(pk=Todos_id)
    todo.finished = False
    todo.finished_date = None
    todo.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def no_finish(request,Todos_id):
    todo = Todos.objects.get(pk=Todos_id)
    todo.finished = True  
    todo.finished_date = datetime.now()
    todo.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def update(request, Todos_id):
    todo_item = get_object_or_404(Todos, pk=Todos_id)

    if request.method == "POST":
        form = ListForm(request.POST, instance=todo_item)
        if form.is_valid():
            todo = form.save(commit=False)
            if todo.finished and not todo.finished_date:
                todo.finished_date = datetime.now()         
            elif not todo.finished:
                todo.finished_date = None

            todo.save()
            return redirect("index")
    else:
        form = ListForm(instance=todo_item)

    return render(request, "todo_app/update.html", {'form': form})


    

@login_required
def description(request, id):
    todo = get_object_or_404(Todos, id=id)
    return render(request, 'todo_app/description.html', {'todo': todo})



@login_required
def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            todos = Todos.objects.filter(category=category).order_by('-date')
        else:
            todos = Todos.objects.filter(
                category=category
            ).filter(
                models.Q(is_private=False) | models.Q(user=request.user)
            ).order_by('-date')
    else:
        todos = Todos.objects.filter(category=category, is_private=False).order_by('-date')
        
    subcategories = Category.objects.filter(parent=category)    

    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.category = category
            new_todo.user = request.user
            new_todo.save()
            return redirect('category_view', category_id=category.id)
    else:
        form = ListForm()

    return render(request, "todo_app/category_view.html", {
        'category': category,
        'todo_list': todos,
        'form': form,
        'subcategories': subcategories,
    })
    
    

@login_required
def add_category(request, parent_id=None):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            if parent_id:
                parent = get_object_or_404(Category, id=parent_id)
                new_category.parent = parent
            new_category.save()
            
            # Ekleme sonrası parent varsa oraya dön
            if new_category.parent:
                return redirect('category_view', category_id=new_category.parent.id)
            return redirect('index')  # parent yoksa anasayfaya dön

    else:
        form = CategoryForm()
        if parent_id:
            parent = get_object_or_404(Category, id=parent_id)
            form.fields['parent'].initial = parent

    return render(request, 'todo_app/add_category.html', {'form': form})



@login_required
def add_todo_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.category = category
            new_todo.user = request.user  
            new_todo.save()
            return redirect('category_view', category_id=category.id)
    else:
        form = ListForm()

    return render(request, "todo_app/add_todo_to_category.html", {
        'form': form,
        'category': category
    })


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('index')  



@login_required
def user_info(request):
    
    user = request.user
    return render(request, 'todo_app/user_info.html', {'user': user})


@login_required
def update_cat(request, Category_id):
    category = get_object_or_404(Category, id=Category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            updated_category = form.save()
            if updated_category.parent:
                return redirect('category_view', category_id=updated_category.parent.id)
            else:
                return redirect('index')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'todo_app/update_category.html', {'form': form, 'category': category})

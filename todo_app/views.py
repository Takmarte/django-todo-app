from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Todos, Category,DailyTodoList, TodoItem
from .forms import TodoForm , CategoryForm, DailyTodoListForm, TodoItemForm
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def todo(request):
    todo_list = Todos.objects.all().order_by('-date_created') if request.user.is_superuser \
                else Todos.objects.filter(models.Q(is_private=False) | models.Q(daily_list__user=request.user)).order_by('-date_created')
    daily_lists = DailyTodoList.objects.all() if request.user.is_superuser else DailyTodoList.objects.filter(user=request.user)
    return render(request, "todo_app/todo.html", {'daily_lists': daily_lists, 'todo_list': todo_list})


 
@login_required
def index(request):
    daily_lists = DailyTodoList.objects.all().order_by('-date') if request.user.is_superuser \
                  else DailyTodoList.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.all()
    return render(request, "todo_app/index.html", {'daily_lists': daily_lists, 'categories': categories})


def about(request):
    return render(request,"todo_app/about.html")

@login_required
def create_redirect_to_today_list(request):
    today = datetime.today().date()
    daily_list, _ = DailyTodoList.objects.get_or_create(
        user=request.user, date=today, defaults={'name': f"My Tasks - {today}"})
    return redirect('daily_list_detail', list_id=daily_list.id)


@login_required
def add_todo_to_daily_list(request, daily_list_id):
    daily_list = get_object_or_404(DailyTodoList, id=daily_list_id, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.daily_list = daily_list
            if todo.finished and not todo.finished_date:
                todo.finished_date = datetime.now()
            todo.save()
            return redirect('daily_list_detail', list_id=daily_list.id)
    else:
        form = TodoForm()
    return render(request, "todo_app/add_todo.html", {'form': form, 'daily_list': daily_list})


@login_required
def delete(request, todo_id):
    todo = get_object_or_404(Todos, id=todo_id)
    daily_list_id = todo.daily_list.id if todo.daily_list else None
    todo.delete()
    return redirect('daily_list_detail', list_id=daily_list_id) if daily_list_id else redirect("index")




@login_required
def yes_finish(request, todo_id):
    todo = get_object_or_404(Todos, pk=todo_id)
    todo.finished = False
    todo.finished_date = None
    todo.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def no_finish(request, todo_id):
    todo = get_object_or_404(Todos, pk=todo_id)
    todo.finished = True
    todo.finished_date = datetime.now()
    todo.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def update(request, todo_id):
    todo_item = get_object_or_404(Todos, pk=todo_id)
    if request.user != todo_item.daily_list.user and not request.user.is_superuser:
        return redirect("index")
    form = TodoForm(request.POST or None, instance=todo_item)
    if request.method == "POST" and form.is_valid():
        todo = form.save(commit=False)
        todo.finished_date = datetime.now() if todo.finished else None
        todo.save()
        return redirect("index")
    return render(request, "todo_app/update.html", {'form': form, 'todo': todo_item})

@login_required
def description(request, id):
    todo = get_object_or_404(Todos, id=id)
    if not request.user.is_superuser and todo.daily_list and todo.daily_list.user != request.user:
        return redirect("index")
    return render(request, 'todo_app/description.html', {
        'todo': todo,
        'todo_items': todo.items.all(),
        'daily_list_id': todo.daily_list.id if todo.daily_list else None,
    })

@login_required
def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.user.is_superuser:
        daily_lists = DailyTodoList.objects.filter(category=category)
    else:
        daily_lists = DailyTodoList.objects.filter(category=category, user=request.user)

    subcategories = category.subcategories.all()

    return render(request, "todo_app/category_view.html", {
        'category': category,
        'daily_lists': daily_lists,
        'subcategories': subcategories,
    })



      
@login_required
def add_category(request, parent_id=None):
    parent = None
    if parent_id:
        parent = get_object_or_404(Category, id=parent_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.parent = parent
            new_category.save()
            return redirect('category_view', category_id=parent.id) if parent else redirect('index')
    else:
        form = CategoryForm(initial={'parent': parent})

    return render(request, 'todo_app/add_category.html', {'form': form})


@login_required
def add_todo_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    daily_list, created = DailyTodoList.objects.get_or_create(
        user=request.user,
        date=datetime.today(),
        category=category,  
        defaults={'name': f'{category.name} - {datetime.today().strftime("%Y-%m-%d")}'}
    )

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.daily_list = daily_list
            new_todo.user = request.user
            new_todo.save()
            return redirect('category_view', category_id=category.id)
    else:
        form = TodoForm()

    return render(request, "todo_app/add_todo_to_category.html", {
        'form': form,
        'category': category
    })


@login_required
@require_POST
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    parent_id = category.parent.id if category.parent else None
    category.delete()

    if parent_id:
        return redirect('category_view', category_id=parent_id)
    return redirect('index')


@login_required
def user_info(request):
    return render(request, 'todo_app/user_info.html', {'user': request.user})


@login_required
def update_cat(request, Category_id):
    category = get_object_or_404(Category, id=Category_id)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        updated_category = form.save()
        parent = updated_category.parent
        return redirect('category_view', category_id=parent.id) if parent else redirect('index')

    return render(request, 'todo_app/update_category.html', {
        'form': form,
        'category': category
    })


@login_required
def create_daily_list(request):
    if request.method == "POST":
        form = DailyTodoListForm(request.POST)
        if form.is_valid():
            daily_list = form.save(commit=False)
            daily_list.user = request.user
            daily_list.save()
            return redirect('daily_list_detail', list_id=daily_list.id)
    else:
        form = DailyTodoListForm()
        
    return render(request, 'todo_app/create_daily_list.html', {'form': form})

@login_required
@login_required
def daily_list_detail(request, list_id):
    daily_list = get_object_or_404(DailyTodoList, id=list_id) if request.user.is_superuser \
                  else get_object_or_404(DailyTodoList, id=list_id, user=request.user)
    todos = daily_list.todos.prefetch_related('items').all()
    form = TodoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        todo = form.save(commit=False)
        todo.daily_list = daily_list
        todo.user = request.user
        todo.finished_date = datetime.now() if todo.finished else None
        todo.save()
        return redirect('daily_list_detail', list_id=daily_list.id)
    return render(request, 'todo_app/daily_list_detail.html', {
        'daily_list': daily_list,
        'todo_list': todos,
        'form': form
    })




@login_required
def add_todo_item(request, todo_id):
    todo = get_object_or_404(Todos, id=todo_id)
    next_url = request.GET.get('next')

    if request.method == "POST":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            text = request.POST.get('text', '').strip()
            if text:
                item = TodoItem.objects.create(todo=todo, text=text)
                return JsonResponse({'success': True, 'id': item.id, 'text': item.text})
            return JsonResponse({'success': False, 'error': 'Text boş olamaz'}, status=400)
 
        form = TodoItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.todo = todo
            item.save()
            if next_url:
                return redirect(next_url)
            else:
                return redirect('description', todo.id)
    else:
        form = TodoItemForm()

    return render(request, 'todo_app/add_todo_item.html', {
        'form': form,
        'todo': todo,
        'next': next_url or reverse('description', args=[todo.id]),
    })
    
    
@login_required
def update_subtask(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)
    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('description', id=item.todo.id)
    else:
        form = TodoItemForm(instance=item)
    return render(request, 'todo_app/update_subtask.html', {'form': form, 'item': item})

@login_required
@require_POST
def delete_subtask(request, item_id):
    item = get_object_or_404(TodoItem, id=item_id)

    if request.user == item.todo.user or request.user.is_superuser:
        if request.method == "POST":
            item.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)

@require_POST
def toggle_subtask_done(request, item_id):
    try:
        item = TodoItem.objects.get(id=item_id)
        item.done = not item.done
        item.save()
        return JsonResponse({'success': True, 'done': item.done })
    except TodoItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
    
@require_POST
@login_required
def toggle_finish_status(request, todo_id):
    try:
        todo = Todos.objects.get(pk=todo_id)
        if request.user == todo.user or request.user.is_superuser:
            todo.finished = not todo.finished
            todo.finished_date = timezone.now() if todo.finished else None
            todo.save()
            return JsonResponse({'status': 'success', 'finished': todo.finished})
        else:
            return JsonResponse({'status': 'unauthorized'}, status=403)
    except Todos.DoesNotExist:
        return JsonResponse({'status': 'not found'}, status=404)
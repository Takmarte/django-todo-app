from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timezone
from django.utils.timezone import now
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subcategories')
 
    def __str__(self):
        prefix = f"{self.parent} > " if self.parent else ""
        return f"{prefix}{self.name}"
    
class DailyTodoList(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='daily_lists')
    name = models.CharField(max_length=100) 
    date = models.DateField(default=datetime.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Todos(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    finished = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now, blank=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_private = models.BooleanField(default=True)
    daily_list = models.ForeignKey('DailyTodoList', on_delete=models.CASCADE, related_name='todos', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def progress(self):
        items = self.items.all()
        total = items.count()
        if total == 0:
            return 0
        done = items.filter(done=True).count()
        return int((done / total) * 100)

    def update_finished_status(self):
        """Tüm alt görevler tamamlandıysa otomatik olarak finished=True yapar."""
        items = self.items.all()
        if items.exists() and all(item.done for item in items):
            self.finished = True
            self.finished_date = timezone.now()
        else:
            self.finished = False
            self.finished_date = None
        self.save()

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    todo = models.ForeignKey(Todos, related_name="items", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.text
# Generated by Django 5.2.3 on 2025-06-25 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_todos_finished_date_alter_todos_finished_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todos',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

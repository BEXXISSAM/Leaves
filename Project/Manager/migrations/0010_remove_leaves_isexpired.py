# Generated by Django 3.2.25 on 2024-05-16 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0009_rename_isexiperd_leaves_isexpired'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaves',
            name='isExpired',
        ),
    ]
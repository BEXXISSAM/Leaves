# Generated by Django 3.2.25 on 2024-05-15 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Manager', '0008_leaves_isexiperd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaves',
            old_name='isExiperd',
            new_name='isExpired',
        ),
    ]
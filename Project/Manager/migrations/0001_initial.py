# Generated by Django 5.0.4 on 2024-04-27 22:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=50)),
                ('isAdmin', models.BooleanField(default=False)),
                ('username', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaveDate', models.DateField()),
                ('duration', models.IntegerField()),
                ('endOfLeave', models.DateField()),
                ('leaveNumber', models.IntegerField()),
                ('isDelayed', models.BooleanField(default=False)),
                ('employeeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manager.employee')),
            ],
        ),
    ]
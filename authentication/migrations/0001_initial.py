# Generated by Django 2.1.7 on 2019-03-16 12:24

import authentication.managers
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estates', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=50, verbose_name='phone')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_owner', models.BooleanField(default=True, verbose_name='is owner')),
                ('is_security', models.BooleanField(default=False, verbose_name='is security')),
                ('is_resident', models.BooleanField(default=False, verbose_name='is resident')),
                ('estate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff', to='estates.Estate')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', authentication.managers.UserManager()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('phone', 'estate')},
        ),
    ]

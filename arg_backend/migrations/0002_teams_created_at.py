# Generated by Django 2.1 on 2021-10-20 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arg_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='created at'),
        ),
    ]

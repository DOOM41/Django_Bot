# Generated by Django 4.2.4 on 2023-08-16 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='chat_id',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='ID чата пользователя в телеграмме'),
        ),
    ]

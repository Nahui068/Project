# Generated by Django 2.1.7 on 2019-03-27 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20190327_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='user_pw',
            field=models.CharField(default='1234', max_length=20),
        ),
    ]

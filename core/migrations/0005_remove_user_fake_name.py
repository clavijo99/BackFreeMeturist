# Generated by Django 4.0.4 on 2023-07-21 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_fake_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fake_name',
        ),
    ]

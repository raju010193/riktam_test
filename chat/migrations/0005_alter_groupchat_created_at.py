# Generated by Django 4.0.5 on 2022-06-28 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_groupmembers_created_at_alter_groups_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupchat',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

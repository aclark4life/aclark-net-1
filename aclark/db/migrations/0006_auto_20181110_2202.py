# Generated by Django 2.1.2 on 2018-11-10 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_project_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='project',
            name='notes',
        ),
    ]

# Generated by Django 2.1.10 on 2019-07-07 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("db", "0026_remove_client_note")]

    operations = [migrations.RemoveField(model_name="project", name="note")]

# Generated by Django 3.1.7 on 2021-03-29 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='concepto',
            field=models.CharField(max_length=250, null=True),
        ),
    ]

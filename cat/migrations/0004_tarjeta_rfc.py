# Generated by Django 3.1.7 on 2021-03-29 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0003_tarjeta_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjeta',
            name='rfc',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
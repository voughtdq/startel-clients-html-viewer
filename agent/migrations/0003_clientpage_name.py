# Generated by Django 4.2 on 2023-06-27 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_auto_20230414_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientpage',
            name='name',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]

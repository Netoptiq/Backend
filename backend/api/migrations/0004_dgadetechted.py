# Generated by Django 5.0 on 2023-12-20 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DGADetechted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=200)),
            ],
        ),
    ]

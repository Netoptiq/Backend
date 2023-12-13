# Generated by Django 5.0 on 2023-12-13 11:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delay', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Domaincount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100)),
                ('count', models.IntegerField(blank=0, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ParsedPacket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('src', models.GenericIPAddressField(blank=True, null=True)),
                ('dst', models.GenericIPAddressField(blank=True, null=True)),
                ('proto', models.CharField(max_length=255)),
                ('len', models.IntegerField()),
                ('sport', models.IntegerField(blank=True, null=True)),
                ('dport', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
                ('record', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
                ('record', models.CharField(max_length=10)),
                ('res_type', models.CharField(max_length=10)),
                ('delay', models.FloatField()),
                ('TSIG', models.FloatField()),
                ('size', models.IntegerField()),
                ('country', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.query')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.reply')),
            ],
        ),
    ]

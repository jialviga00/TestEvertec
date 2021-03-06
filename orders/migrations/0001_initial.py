# Generated by Django 3.0.5 on 2021-04-07 02:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=80)),
                ('customer_email', models.CharField(max_length=120)),
                ('customer_mobile', models.CharField(max_length=40)),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(verbose_name='Updated at')),
            ],
        ),
    ]

# Generated by Django 3.0.5 on 2021-04-07 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210407_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='placetopay_process_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='placetopay_request_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='reference',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

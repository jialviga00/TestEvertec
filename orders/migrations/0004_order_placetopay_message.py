# Generated by Django 3.0.5 on 2021-04-08 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210407_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='placetopay_message',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

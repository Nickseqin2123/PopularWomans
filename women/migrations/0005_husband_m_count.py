# Generated by Django 4.2.11 on 2024-05-16 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0004_husband_women_husband'),
    ]

    operations = [
        migrations.AddField(
            model_name='husband',
            name='m_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]

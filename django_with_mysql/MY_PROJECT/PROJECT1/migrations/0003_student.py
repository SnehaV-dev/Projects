# Generated by Django 5.1.1 on 2024-10-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECT1', '0002_details_depart_details_year_of_joining'),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('std', models.CharField(max_length=20)),
                ('grade', models.CharField(max_length=20)),
            ],
        ),
    ]

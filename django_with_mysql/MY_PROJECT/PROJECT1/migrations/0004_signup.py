# Generated by Django 5.1.1 on 2024-10-19 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECT1', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
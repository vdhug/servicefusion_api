# Generated by Django 2.0 on 2020-01-30 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=125)),
                ('address_line_2', models.CharField(max_length=125)),
                ('address_line_3', models.CharField(max_length=125)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=60)),
                ('postal_code', models.CharField(max_length=16)),
            ],
        ),
    ]

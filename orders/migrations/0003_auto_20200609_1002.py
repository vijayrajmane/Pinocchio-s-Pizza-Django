# Generated by Django 3.0.7 on 2020-06-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_topping'),
    ]

    operations = [
        migrations.CreateModel(
            name='pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='salad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='sub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('small_price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('large_price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.RemoveField(
            model_name='pizza',
            name='category',
        ),
    ]
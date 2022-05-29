# Generated by Django 3.1.8 on 2022-05-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_remove_feature_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]

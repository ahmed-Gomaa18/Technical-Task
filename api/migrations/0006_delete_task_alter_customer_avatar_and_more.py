# Generated by Django 4.0.4 on 2022-05-29 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_customer_created_customer_updated_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='birthdate',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='country_code',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='customer',
            name='otp',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, unique=True),
        ),
    ]

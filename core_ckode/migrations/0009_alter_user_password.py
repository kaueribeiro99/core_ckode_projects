# Generated by Django 4.2.2 on 2023-06-12 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_ckode', '0008_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]

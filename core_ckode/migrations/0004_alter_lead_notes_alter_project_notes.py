# Generated by Django 4.2.2 on 2023-06-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_ckode', '0003_alter_lead_notes_alter_project_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]

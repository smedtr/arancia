# Generated by Django 4.1.4 on 2023-01-31 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objectives', '0007_alter_objective_domain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objective',
            name='domain',
            field=models.CharField(choices=[('Execution', 'Execution'), ('Education', 'Education'), ('Template', 'Template')], default='Execution', max_length=10),
        ),
    ]

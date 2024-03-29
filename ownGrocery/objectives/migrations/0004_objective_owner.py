# Generated by Django 4.1.4 on 2023-01-31 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_worker_account'),
        ('objectives', '0003_alter_objective_ref_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='objective',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objective_owner', to='teams.worker', verbose_name='owner'),
        ),
    ]

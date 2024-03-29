# Generated by Django 4.1.4 on 2023-01-19 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0008_worker_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_period', models.CharField(max_length=255)),
                ('stage', models.CharField(choices=[('START', 'Start Objectives'), ('SET-OBJ', 'Set Objectives'), ('RUN-OBJ', 'Execute Objectives'), ('CALIB-MIDYEAR', 'Calibration for MidYear'), ('MIDYEAR', 'MidYear'), ('CALIB-ENDYEAR', 'Calibration for MidYear'), ('ENDYEAR', 'EndYear'), ('CLOSE-OBJ', 'Close')], db_index=True, max_length=15)),
                ('description', models.TextField(blank=True, null=True)),
                ('score', models.JSONField(default=dict)),
                ('setobjectives_at', models.DateField(blank=True, null=True)),
                ('objectives_approval_at', models.DateField(blank=True, null=True)),
                ('midyear_at', models.DateField(blank=True, null=True)),
                ('endyear_at', models.DateField(blank=True, null=True)),
                ('endyear_approval_at', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objectives', to='teams.worker', verbose_name='employee')),
            ],
        ),
    ]

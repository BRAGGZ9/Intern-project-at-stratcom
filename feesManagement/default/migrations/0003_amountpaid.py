# Generated by Django 4.2.2 on 2023-06-12 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_levels'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountPaid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='default.levels')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='default.userprofile')),
            ],
        ),
    ]

# Generated by Django 4.2 on 2024-10-02 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlySummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('encouragement_message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_plans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('child', 'parent', 'year', 'month')},
            },
        ),
        migrations.DeleteModel(
            name='MothlySummary',
        ),
    ]

# Generated by Django 4.2 on 2024-09-26 02:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0002_remove_financediary_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financediary',
            name='expenditure',
        ),
        migrations.RemoveField(
            model_name='financediary',
            name='income',
        ),
        migrations.RemoveField(
            model_name='financediary',
            name='title',
        ),
        migrations.AddField(
            model_name='financediary',
            name='amount',
            field=models.PositiveIntegerField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='financediary',
            name='category',
            field=models.CharField(choices=[('ALLOWANCE', '용돈'), ('BONUS', '추가 용돈'), ('CHORES_EARNINGS', '용돈 벌이'), ('PRIZES', '상금/포상금'), ('SNACK', '간식비'), ('TOYS', '게임/장난감비'), ('BOOKS', '책/학용품비'), ('TRANSPORT', '교통비'), ('EXTRACURRICULAR', '학원비'), ('ENTERTAINMENT', '문화/오락비'), ('GIFT', '선물비'), ('ETC', '기타')], max_length=20),
        ),
    ]

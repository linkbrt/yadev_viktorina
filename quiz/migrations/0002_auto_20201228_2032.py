# Generated by Django 3.1.4 on 2020-12-28 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('choise', 'Choise'), ('input', 'Input')], default='input', max_length=50),
        ),
    ]
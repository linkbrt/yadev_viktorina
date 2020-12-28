# Generated by Django 3.0.5 on 2020-12-27 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20201227_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_input',
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('choise', 'Choise'), ('input', 'Input')], default='input', max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(verbose_name='Текст вопроса'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Quiz', verbose_name='Викторина'),
        ),
    ]
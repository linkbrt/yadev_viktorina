# Generated by Django 3.0.5 on 2020-12-27 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название викторины')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание викторины')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='ЧПУ')),
                ('success_page', models.FileField(blank=True, null=True, upload_to='pages/', verbose_name='Страница с поздравлением')),
                ('image', models.ImageField(blank=True, null=True, upload_to='quiz_images/', verbose_name='Изображение викторины')),
            ],
            options={
                'verbose_name': 'Викторина',
                'verbose_name_plural': 'Викторины',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержание вопроса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='questions_images/', verbose_name='Изображение вопроса')),
                ('is_input', models.BooleanField(default=False, verbose_name='Является полем ввода')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Quiz', verbose_name='Викторина')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='Ответ')),
                ('is_right', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.Question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]

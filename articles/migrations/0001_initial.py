# Generated by Django 3.2.4 on 2021-06-26 18:45

import articles.utils
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=articles.utils.get_timestamp_path)),
                ('caption', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Подпись')),
            ],
            options={
                'verbose_name': 'Дополнительная иллюстрация',
                'verbose_name_plural': 'Дополнительные иллюстрации',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=articles.utils.get_timestamp_path)),
                ('title', models.CharField(max_length=40, verbose_name='Название статьи')),
                ('content', models.TextField(verbose_name='Текст статьи')),
                ('source', models.TextField(verbose_name='Источник')),
                ('characters', models.TextField(error_messages={'invalid': 'Введите в формате: "<имя> (<год_рождения>-<год_смерти>)"'}, validators=[django.core.validators.RegexValidator(regex='(.+\\s{1}\\(\\d{4}\\-(?:\\d{4}|\\d{0})\\)(\\,\\s)?)+')], verbose_name='Упоминаются')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Показывать в списке')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='BaseRubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Название')),
                ('slug', models.CharField(max_length=30, unique=True, verbose_name='slug')),
                ('order', models.SmallIntegerField(db_index=True, default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Рубрика',
                'verbose_name_plural': 'Рубрики',
                'ordering': ('super_rubric__order', 'order'),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(verbose_name='Содержание')),
                ('is_approved', models.BooleanField(db_index=True, default=False, verbose_name='Одобрено')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('rating_change', models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike'), (0, 'Neutral')], default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
            ],
        ),
    ]
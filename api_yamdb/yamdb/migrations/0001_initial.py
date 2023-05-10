# Generated by Django 3.2 on 2023-03-27 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='Введите ссылку', unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название жанра', max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(help_text='Введите ссылку', unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название произведения', max_length=256, verbose_name='Название произведения')),
                ('year', models.IntegerField(help_text='Введите год выпуска', verbose_name='Год выпуска')),
                ('rating', models.PositiveSmallIntegerField(default=None, help_text='Введите рейтинг произведения', null=True, verbose_name='Рейтинг')),
                ('description', models.TextField(blank=True, help_text='Введите описание', null=True, verbose_name='Описание')),
                ('category', models.ForeignKey(default=None, help_text='Выберите категорию', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='titles', to='yamdb.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Укажите жанры', related_name='titles', to='yamdb.Genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
    ]

from django.contrib.auth import get_user_model
from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость'
    )
    # TODO

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        verbose_name='курс'
    )
    # TODO

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    name = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        verbose_name='курс'
    )
    student = models.ManyToManyField(
        to=get_user_model(),
        verbose_name='студенты'
    )

    # TODO

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

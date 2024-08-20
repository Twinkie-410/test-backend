from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from courses.models import Course, Group
from users.models import Subscription, Balance


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        group_min = (instance.course.groups.prefetch_related("student").
                     annotate(count=Count('student')).
                     order_by('count').
                     first()
                     )
        group_min.student.add(instance.user)


@receiver(post_save, sender=get_user_model())
def post_save_subscription(sender, instance: get_user_model(), created, **kwargs):
    """
    Создание баланса для студента.

    """

    if created:
        Balance.objects.create(user=instance)


@receiver(post_save, sender=Course)
def post_save_subscription(sender, instance: Course, created, **kwargs):
    """
    Создание групп при создании курса.

    """

    if created:
        Group.objects.bulk_create(
            [Group(title=f'{instance.title} - 1', course=instance),
             Group(title=f'{instance.title} - 2', course=instance),
             Group(title=f'{instance.title} - 3', course=instance),
             Group(title=f'{instance.title} - 4', course=instance),
             Group(title=f'{instance.title} - 5', course=instance),
             Group(title=f'{instance.title} - 6', course=instance),
             Group(title=f'{instance.title} - 7', course=instance),
             Group(title=f'{instance.title} - 8', course=instance),
             Group(title=f'{instance.title} - 9', course=instance),
             Group(title=f'{instance.title} - 10', course=instance)]
        )

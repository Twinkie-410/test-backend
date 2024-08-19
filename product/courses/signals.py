from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        group_min = (instance.course.group_set.prefetch_related("student").
                     annotate(count=Count('student_set__id')).
                     order_by('count').
                     first()
                     )
        group_min.student.add(instance.user)
        # TODO

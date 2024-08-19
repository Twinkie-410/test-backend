from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request):
    # TODO
    pass


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return Subscription.objects.filter(user=request.user).exist() or request.user.is_staff
        # TODO

    def has_object_permission(self, request, view, obj):
        return Subscription.objects.filter(user=request.user).exist() or request.user.is_staff
        # TODO


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS

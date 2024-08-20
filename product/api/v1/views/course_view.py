from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin, make_payment
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)

from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        queryset = self.queryset.exclude(subscription__user=request.user)
        try:
            course = queryset.get(id=pk)
        except Course.DoesNotExist:
            return Response(
                data={"detail": "No Course matches the given query."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not make_payment(request, course.price):
            return Response(
                data={"fail": "insufficient funds"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Subscription.objects.create(
            user=request.user,
            course=course
        )

        return Response(
            data={"OK": "Success"},
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available(self, request):
        "Доступные курсы"
        courses = self.queryset.exclude(subscription__user=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

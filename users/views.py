from django.db.models import IPAddressField
from rest_framework.generics import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.views import APIView, Response
from .serializers import (
    GroupSerializer,
    GroupForUserSerializer,
    UserSerializer,
    UserUpdateSerializer,
    UserSelfUpdateSerializer,
    GroupAddTeacherSerializer,
    GroupAddStudentSerializer,
    UserSerializerForSwagger
)
from .permissions import IsAdminUser, IsTeacherUser
from .models import Group, User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class TeacherRegisterApiView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Teacher Register",
        request_body=UserSerializerForSwagger,
        responses={
            200: UserSerializerForSwagger
        }
    )
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'teacher'
        teacher_ser = UserSerializer(data = data)
        teacher_ser.is_valid(raise_exception=True)
        teacher_ser.save()
        return Response(teacher_ser.data)
        
class StudentRegisterApiView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Student Register",
        request_body=UserSerializerForSwagger,
        responses={
            200: UserSerializer
        }
    )
    def post(self, request):
        data = request.data.copy()
        student_ser = UserSerializer(data = data)
        student_ser.is_valid(raise_exception=True)
        student_ser.save()
        return Response(student_ser.data)

class UserSelfUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserSerializer
        return UserSelfUpdateSerializer

class TeachersListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role = 'teacher')
    serializer_class = UserSerializer

class TeacherRetrieveApiView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role='teacher')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserSerializer
        return UserUpdateSerializer

class StudentsListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(role = 'student')
    serializer_class = UserSerializer

class StudentRetrieveApiView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role = 'student')

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserSerializer
        return UserUpdateSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['add_teacher', 'remove_teacher']:
            return [IsAdminUser()]
        return [(IsAdminUser | IsTeacherUser)()]

    @swagger_auto_schema(
        operation_description="Add teacher to group",
        request_body=GroupAddTeacherSerializer
    )
    @action(detail=True, methods=['post'], url_path='add-teacher')
    def add_teacher(self, request, pk=None):
        group = self.get_object()
        teacher_id = self.request.data.get('teacher_id')
        teacher = get_object_or_404(User, id=teacher_id, role='teacher')

        teacher.groups.add(group)

        return Response(
            {'msg': "Teacher added succesfully."},
            status=200
        )

    @swagger_auto_schema(
        operation_description="Add student to group",
        request_body=GroupAddStudentSerializer
    )
    @action(detail=True, methods = ["post"], url_path="add-student")
    def add_student(self, request, pk=None):
        group = self.get_object()
        student_id = self.request.data.get('student_id')
        student = get_object_or_404(User, id=student_id, role='student')

        student.groups.add(group)

        return Response(
            {"msg": "Student added succesfully."},
            status=200
        )

    @swagger_auto_schema(
        operation_description="Remove teacher from group",
        request_body=GroupAddTeacherSerializer
    )
    @action(detail=True, methods = ['post'], url_path="remove-teacher")
    def remove_teacher(self, request, pk=None):
        group = self.get_object()
        teacher_id = self.request.data.get('teacher_id')
        teacher = get_object_or_404(User, id=teacher_id, role='teacher')

        if group in teacher.groups.all():
            teacher.groups.remove(group)

        return Response(
            {'msg': "Teacher removed succesfully."},
            status=200
        )

    @swagger_auto_schema(
        operation_description="Student remove from group",
        request_body=GroupAddStudentSerializer
    )
    @action(detail=True, methods = ['post'], url_path='remove-student')
    def remove_student(self, request, pk=None):
        group = self.get_object()
        student_id = self.request.data.get('student_id')
        student = get_object_or_404(User, id=student_id, role='student')

        if group in student.groups.all():
            student.groups.remove(group)

        return Response(
            {"msg": "Student has been removed succesfully"},
            status=200
        )

    @swagger_auto_schema(
        operation_description="Teachers of group",
        responses={
            200: UserSerializer
        }
    )
    @action(detail=True, methods = ['get'])
    def teachers(self, request, pk=None):
        group = self.get_object()
        teachers = group.members.filter(role='teacher')
        teachers_ser = UserSerializer(teachers, many=True)
        return Response(teachers_ser.data)

    @swagger_auto_schema(
        operation_description="Students of group",
        responses={
            200: UserSerializer
        },
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                required=False,
                type = openapi.TYPE_INTEGER
            )
        ]
    )
    @action(detail=True,methods=['get'])
    def students(self, request, pk=None):
        group = self.get_object()
        students = group.members.filter(role='student')

        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(
            students,
            request
        )

        serializer = UserSerializer(
            page, many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

class TeacherGroupsListApiView(APIView):
    permission_classes = [IsAdminUser | IsTeacherUser]
    @swagger_auto_schema(
        operation_description="Groups of teacher",
        responses={
            200: GroupForUserSerializer
        }
    )
    def get(self, request, pk):
        teacher = get_object_or_404(User, id=pk, role='teacher')
        groups = teacher.groups.all()
        groups_ser = GroupForUserSerializer(groups, many=True)
        return Response(groups_ser.data)

class StudentGroupsListApiView(APIView):
    permission_classes = [IsAdminUser | IsTeacherUser]
    @swagger_auto_schema(
        operation_description="Groups of student",
        responses={
            200: GroupForUserSerializer
        }
    )
    def get(self, request, pk):
        student = get_object_or_404(User, id=pk, role='student')
        groups = student.groups.all()
        groups_ser = GroupForUserSerializer(groups, many=True)
        return Response(groups_ser.data)
        
class UserSelfGroupsListApiView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Groups",
        responses={
            200: GroupForUserSerializer
        }
    )
    def get(self, request):
        user = request.user
        groups = user.groups.all()
        groups_ser = GroupForUserSerializer(groups, many=True)
        return Response(groups_ser.data)

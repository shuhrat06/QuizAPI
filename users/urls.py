from django.urls import include, path
from .views import (
    TeacherRegisterApiView,
    StudentRegisterApiView,
    UserSelfUpdateDeleteApiView,
    TeacherRetrieveApiView,
    StudentRetrieveApiView,
    TeachersListApiView,
    StudentsListApiView,
    GroupViewSet,
    TeacherGroupsListApiView,
    StudentGroupsListApiView,
    UserSelfGroupsListApiView,
)
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh
from rest_framework.routers import DefaultRouter

rtr = DefaultRouter()
rtr.register('groups', GroupViewSet)

urlpatterns = [
    path('register/teacher/', TeacherRegisterApiView.as_view()),
    path('register/student/', StudentRegisterApiView.as_view()),
    path('user/token/obtain/', token_obtain_pair),
    path('user/token/refresh/', token_refresh),
    path('user/profile/', UserSelfUpdateDeleteApiView.as_view()),
    path('user/my-groups/', UserSelfGroupsListApiView.as_view()),
    
    path('teachers/', TeachersListApiView.as_view()),
    path('teachers/<int:pk>/groups', TeacherGroupsListApiView.as_view()),
    path('teachers/<int:pk>/', TeacherRetrieveApiView.as_view()),

    path('students/', StudentsListApiView.as_view()),
    path('students/<int:pk>/groups/', StudentGroupsListApiView.as_view()),
    path('students/<int:pk>/', StudentRetrieveApiView.as_view()),

    path('', include(rtr.urls)),
]

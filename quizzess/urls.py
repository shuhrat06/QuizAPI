from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet,
    QuizAddQuestionApiView,
    QuizQuestionsListApiView,
    QuizRemoveQuestionsApiView,
    QuestionRetrieveApiView,
    OptionRetrieveApiView,
    AllowedStudentsListApiView,
    AllowedStudentsAddListApiView,
    
)

rtr = DefaultRouter()
rtr.register('quizzes', QuizViewSet)

urlpatterns = [
    path('quizzes/<int:pk>/add-question/', QuizAddQuestionApiView.as_view()),
    path('quizzes/<int:pk>/questions/', QuizQuestionsListApiView.as_view()),
    path('quizzes/<int:pk>/remove-questions/',QuizRemoveQuestionsApiView.as_view()),
    path('quizzes/<int:pk>/allowed-students/', AllowedStudentsListApiView.as_view()),
    path('quizzes/<int:pk>/allowed-students/add/', AllowedStudentsAddListApiView.as_view()),
    path('', include(rtr.urls)),

    path('questions/<int:pk>/', QuestionRetrieveApiView.as_view()),
    path('options/<int:pk>/',OptionRetrieveApiView.as_view()),
]

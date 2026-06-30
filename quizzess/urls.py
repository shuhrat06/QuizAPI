from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet,
    QuizAddQuestionApiView,
)

rtr = DefaultRouter()
rtr.register('quizzes', QuizViewSet)

urlpatterns = [
    path('quizzes/<int:pk>/add-question/', QuizAddQuestionApiView.as_view()),
    path('', include(rtr.urls)),
]

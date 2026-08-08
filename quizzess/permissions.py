from rest_framework.permissions import BasePermission

class IsOwnerofQuiz(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

class IsOwnerofQuestion(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.quiz.created_by == request.user

class IsOwnerofOption(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.question.quiz.created_by == request.user
        

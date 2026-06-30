from django.contrib import admin

from .models import (
    Quiz,
    Question,
    Option,
    Submission,
    StudentAnswer
)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'created_by',
        'start_time',
        'end_time',
        'is_active',
    ]

    list_filter = [
        'is_active',
        'start_time',
        'end_time',
    ]

    search_fields = [
        'title',
        'created_by__username',
    ]

    filter_horizontal = [
        'allowed_students',
    ]

    inlines = [
        QuestionInline,
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'quiz',
        'text',
    ]

    search_fields = [
        'text',
        'quiz__title',
    ]

    inlines = [
        OptionInline,
    ]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'question',
        'text',
        'is_correct',
    ]

    list_filter = [
        'is_correct',
    ]

    search_fields = [
        'text',
        'question__text',
    ]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'quiz',
        'student',
        'submitted_at',
    ]

    list_filter = [
        'quiz',
        'submitted_at',
    ]

    search_fields = [
        'student__username',
        'quiz__title',
    ]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'submission',
        'question',
        'selected_option',
    ]

    search_fields = [
        'submission__student__username',
        'question__text',
    ]

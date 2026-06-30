from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

    search_fields = [
        'name',
    ]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'id',
        'username',
        'first_name',
        'last_name',
        'role'
    ]

    list_filter = [
        'role'
    ]

    search_fields = [
        'username',
        'first_name',
        'last_name',
    ]

    fieldsets = UserAdmin.fieldsets + (
        (
            'Extra information',
            {
                'fields': (
                    'role',
                )
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Extra information',
            {
                'fields': (
                    'role',
                    'groups',
                )
            }
        ),
    )

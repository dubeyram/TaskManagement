from django.contrib import admin
from user_tasks.models import Task, User


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "created_at", "completed_at")
    list_filter = ("status", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "date_joined", "is_active")
    list_filter = ("is_active", "date_joined")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)


admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAdmin)

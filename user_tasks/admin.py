from django.contrib import admin
from user_tasks.models import Task, User

# Register your models heree


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)


admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAdmin)

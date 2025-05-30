from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('user_type', 'is_active', 'is_staff')
    ordering = ('username',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
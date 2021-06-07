from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):  # TODO programmatically create groups (workers, clients) and permissions
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        'username', 'email', 'is_active', 'mobile', 'name', 'is_worker', 'is_client'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_worker', 'is_client', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('mobile', 'avatar', 'name', 'is_client', 'is_worker')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'name',)
    ordering = ('email', 'username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)

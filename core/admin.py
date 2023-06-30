from django.contrib import admin
from core.models import User, Category, Site, Comment, SocialNetwork, SiteImages, Recommended
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    """ admin para modelo user custom """
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'avatar', 'phone', 'nationality', 'gender')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'avatar', 'phone', 'nationality', 'gender')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Site)
admin.site.register(Comment)
admin.site.register(SocialNetwork)
admin.site.register(SiteImages)
admin.site.register(Recommended)

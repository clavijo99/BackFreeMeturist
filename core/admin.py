from django.contrib import admin
from core.models import User, Category, Site, Comment, SocialNetwork, SiteImages, Recommended
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    """ admin para modelo user custom """
    ordering = ['id']
    list_display = ['email', 'name',]
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


@admin.register(SiteImages)
class SiteImagesAdmin(admin.ModelAdmin):
    list_display=('site',)
    


@admin.register(Recommended)
class Recommended(admin.ModelAdmin):
    list_display=('title',)




@admin.register(SocialNetwork)
class SocialNetwork(admin.ModelAdmin):
    list_display=('site','link','type_social_network',)

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Site)
admin.site.register(Comment)
#admin.site.register(SocialNetwork)
#admin.site.register(Recommended)
#admin.site.register(SiteImages)




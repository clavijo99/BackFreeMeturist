from django.contrib import admin
from core.models import User, Category, Site, Comment, SocialNetwork, SiteImages, Recommended
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from django.contrib import admin
from .models import Comment




class UserAdmin(BaseUserAdmin):
    """ admin para modelo user custom """
    ordering = ['id']
    list_display = ['email', 'name', 'nationality', 'created',]
    search_fields=['name',]
    list_per_page = 10
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
    search_fields = ['site__name',]
    
    


@admin.register(Recommended)
class Recommended(admin.ModelAdmin):
    list_display=('title',)




@admin.register(SocialNetwork)
class SocialNetwork(admin.ModelAdmin):
    list_display=('site','link','type_social_network',)




#Funtion para no mostrar todo el comentario si es muyy extenso
def truncated_comment(obj):
    return obj.name[:120] if len(obj.name) > 120 else obj.name
truncated_comment.short_description = 'Comentario'

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display=('get_truncated_comment', 'site', 'user', 'quality',)
    search_fields=['site__name',]
    list_per_page = 10

    def get_truncated_comment(self, obj):
        return truncated_comment(obj)
    get_truncated_comment.short_description = truncated_comment.short_description

    




@admin.register(Site)
class Site(admin.ModelAdmin):
    list_display=('name', 'location', 'address', 'quality',)
    search_fields=['name',]
    list_per_page = 10



admin.site.register(User,UserAdmin)
#admin.site.register(User, UserAdmin)
admin.site.register(Category)
#admin.site.register(Site)
#admin.site.register(Comment)
#admin.site.register(SocialNetwork)
#admin.site.register(Recommended)
#admin.site.register(SiteImages)




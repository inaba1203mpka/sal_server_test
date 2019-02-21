from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *

@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name','last_name', 'email','phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name','last_name',  'is_staff')
    search_fields = ('username', 'first_name','last_name',  'email')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Reservation)
admin.site.register(Facility)
admin.site.register(Room)
admin.site.register(UseKind)
admin.site.register(Area)

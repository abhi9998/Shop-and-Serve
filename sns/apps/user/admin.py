from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models


class SnsUserAdmin(BaseUserAdmin):
    ordering = ['id']

    # fields to be included in list users page
    list_display = ['email', 'name', 'mobile', 'address', 'city',
                    'verifystatus', 'registeredat', 'walletamount', 'pincode']

    # fields to be included on change user page (edit page)
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        (_('Personal Info'), {'fields': ('name', 'address', 'city', 'pincode')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_superuser')
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # fields to be included in add user page
    # therefore we can create a new user with email and password
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile', 'address', 'city', 'pincode', 'password')
        }),
    )

    search_fields = ('email',)

admin.site.register(models.SnsUser, SnsUserAdmin)
admin.site.register(models.Group)
admin.site.register(models.GroupMembership)
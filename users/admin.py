from django.contrib import admin
from .models import User
from allauth.account.admin import EmailAddressAdmin
# from dj_rest_auth.models import T
from rest_framework.authtoken.admin import TokenAdmin,TokenProxy
# Register your models here.
admin.site.site_title = 'OPPS ADMINISTRATION SITE'
admin.site.site_header = 'OPPS ADMINISTRATION'
admin.site.index_title = 'OPPS ADMINISTRATION'

class UserAdmin(admin.ModelAdmin):
    list_display = ["firstname","lastname","category","role","email"]
# admin.site.name = 'mike'
admin.site.register(User,UserAdmin)

# admin.site.unregister(TokenAdmin,TokenProxy)
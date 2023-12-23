from django.contrib import admin
from .models import User

# Register your models here.
admin.site.site_title = 'OPPS ADMINISTRATION SITE'
admin.site.site_header = 'OPPS ADMINISTRATION'
admin.site.index_title = 'OPPS ADMINISTRATION'
# admin.site.name = 'mike'
admin.site.register(User)
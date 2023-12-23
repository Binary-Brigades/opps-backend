from django.contrib import admin


from . import models
# Register your models here.
# admin.site.site_title('OPPS ADMINISTRATION SITE')


admin.site.register(models.Answer)
admin.site.register(models.Category)
admin.site.register(models.Question)
admin.site.register(models.Review)
admin.site.register(models.Template)
admin.site.register(models.Proposal)
admin.site.register(models.Assignment)

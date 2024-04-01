from django.contrib import admin


from . import models
# Register your models here.
# admin.site.site_title('OPPS ADMINISTRATION SITE')


class AssigmentAdmin(admin.ModelAdmin):
    list_display = ["reviewer","proposal"]
class ProposalAdmin(admin.ModelAdmin):
    list_display = ["template","proposer","created_on","status","assigned"]
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question","template","marks","max_words"]
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["category","title"]
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["proposal","question","answer"]
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["reviewer","proposal","comments","marks"]


admin.site.register(models.Answer,AnswerAdmin)
admin.site.register(models.Category)
admin.site.register(models.Question,QuestionAdmin)
admin.site.register(models.Review,ReviewAdmin)
admin.site.register(models.Template,TemplateAdmin)
admin.site.register(models.Proposal,ProposalAdmin)
admin.site.register(models.Assignment,AssigmentAdmin)

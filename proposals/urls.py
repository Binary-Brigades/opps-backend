from django.urls import path,include
from rest_framework.routers import DefaultRouter
import dj_rest_auth
from . import views

router = DefaultRouter()
router.register('',views.TemplateViewSet,basename='template')

urlpatterns = [
    path('template/',include(router.urls)),
    path('add_proposal/',views.create_proposal,name='add_proposal'),
    path('my_proposal/',views.get_my_proposals,name='my_proposals'),
    path('assign/',views.AssignmentApiView.as_view(),name='assign_proposals'),
    path('reviewers/',views.assign_proposal,name='assign_proposals'),
    path('add_proposal/answer/',views.AnswerAPIView.as_view(),name='answer'),
    path('preview_proposal/<str:id>/',views.view_my_proposal_answers,name='preview-answers'),
    path('get_questions/<str:id>/',views.get_questions,name='questions'),
    path('templates/<str:cat>/',views.get_templates,name='templates'),
    path('review/<str:id>',views.get_proposal_review,name='proposal-review'),
    path('assignments/',views.get_my_assignments,name='my-assignments'),
    path('review/add/<str:id>',views.add_review,name='add-review'),
]

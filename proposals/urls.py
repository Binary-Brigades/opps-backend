from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('',views.TemplateViewSet,basename='template')

urlpatterns = [
    path('template/',include(router.urls)),
    path("assign1/",views.assignProposal),
    path('add_proposal/',views.create_proposal,name='add_proposal'),
    path('my_proposal/',views.get_my_proposals,name='my_proposals'),
    path('assign/',views.AssignmentApiView.as_view(),name='assign_proposals'),
    path('reviewers/',views.assign_proposal,name='assign_proposals'),
    path('add_proposal/answer/',views.add_answers,name='answer'),
    path('proposal_statistics/', views.proposal_statistics, name = 'proposal_statistics'),
    path('preview_proposal/<str:id>/',views.view_my_proposal_answers,name='preview-answers'),
    path('get_questions/<str:id>/',views.get_questions,name='questions'),
    path('create_questions/',views.createQuestions,name='questions_create'),
    path('templates/<str:cat>/',views.get_templates,name='templates'),
    path('review/<str:id>',views.get_proposal_review,name='proposal-review'),
    path('assignments/',views.get_my_assignments,name='my-assignments'),
    path('review/add/<str:id>',views.add_review,name='add-review'),
]

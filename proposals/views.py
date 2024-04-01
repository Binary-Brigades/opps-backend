from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,CreateAPIView)
from drf_yasg.utils import swagger_auto_schema

from . import models
from . import serializers
from users.serializers import CategorySerializer,UserDetailsSerializer
from users.models import Category,User

class CategoryAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
class TemplateViewSet(ModelViewSet):
    serializer_class = serializers.TemplateSerializer
    queryset = models.Template.objects.all()

@swagger_auto_schema(
    method='POST',
    request_body=serializers.ProposalSerializer,
    operation_description='Creates a proposal from a template'
)
@api_view(['POST'])
def create_proposal(request):   
    data = request.data
    print(data)
    data['proposer'] = request.user.id
    serializer = serializers.ProposalSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@swagger_auto_schema(
    method='GET',
    responses={200:serializers.ProposalSerializer(many=True)},
    operation_description='returns a list of proposals created by the user'
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_proposals(request):
    proposals = models.Proposal.objects.filter(proposer=request.user.id)
    serializer = serializers.ProposalSerializer(proposals,many=True)
    if serializer.data:
        return Response(serializer.data)
    return Response({'message':'You have no proposals at the moment'})


class AssignmentApiView(CreateAPIView):
    serializer_class = serializers.AssignmentSerializer
    queryset = models.Assignment.objects.all()

@swagger_auto_schema(
    method='GET',
    operation_description='returns a list of proposals and reviewers for the given category'
)
@api_view(['GET'])
def assign_proposal(request):
    cat = request.user.category
    print(cat)
    reviewers = models.User.objects.filter(category=cat).filter(role='reviewer')
    proposals = models.Proposal.objects.filter(assigned=False).filter(template__category = cat)
    proposals_serializer = serializers.ProposalSerializer(proposals,many=True)
    reviewers_serializer = UserDetailsSerializer(reviewers,many=True)
    return Response({
        'proposals':proposals_serializer.data,
        'reviewers':reviewers_serializer.data
    })

@api_view(["POST"])
def assignProposal(request):
    data = request.data
    proposal = models.Proposal.objects.get(pk=data["proposal"])
    
    reviewer = models.User.objects.get(pk=data["reviewer"])
    # data = {
    #     "proposal":proposal,
    #     "reviewer": reviewer
    # }
    serializer = serializers.AssignmentSerializer(data=data)
    if serializer.is_valid():

        serializer.save()
        proposal.assigned = True
        proposal.save()
        return Response(serializer.data)
    print("proposal ",proposal)
    print("reviewer ",reviewer)
    return Response(serializer.errors)

@swagger_auto_schema(
    method='GET',
    responses={
        201:serializers.AnswerSerializer(many=True),
        404:'not found'
    },
    operation_description='returns a list of answers for the given proposal'
)  
@api_view(['GET'])
def view_my_proposal_answers(request,id):
    try:
        proposal = models.Proposal.objects.get(pk=id)
        # proposal = get_object_or_404()
        template = proposal.template
        questions = models.Question.objects.filter(template=template)
        answers = models.Answer.objects.filter(proposal=proposal.pk)
        quiz_serializer = serializers.QuestionSeriliazer(questions,many=True)
        ans_serializer = serializers.AnswerSerializer(answers,many=True)
            
        response = {
            'title': template.title,
            'questions':quiz_serializer.data,
            'answers': ans_serializer.data
        }
        return Response(response)
    except models.Proposal.DoesNotExist:
        return Response({"message":"Proposal Does Not Exists"},status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='GET',
    responses = {
        201:serializers.QuestionSeriliazer(many=True),
    },
    operation_description='returns a list of questions for the given template'
)
@api_view(['GET'])
def get_questions(request,id):
    questions = models.Question.objects.filter(template=id)
    serializer = serializers.QuestionSeriliazer(questions,many=True)
    template = models.Template.objects.get(pk=id)
    title = template.title
    res ={
        'title':title,
        'questions':serializer.data
    }
    return Response(res)

@swagger_auto_schema(
    method='GET',
    responses = {
        201:serializers.TemplateSerializer,
    },
    operation_description='returns a list of templates for the given category'
)
@api_view(['GET'])
def get_templates(request,cat):
    templates = models.Template.objects.filter(category=cat)
    serializer = serializers.TemplateSerializer(templates,many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET',
    responses = {200: serializers.ProposalSerializer,},    
    operation_description='returns the reviiews made to the proposal'
)
@api_view(['GET'])
def get_proposal_review(request,id):
    try:
        review = models.Review.objects.get(proposal=id)
        serializer = serializers.ReviewSerializer(review)
    except models.Review.DoesNotExist:
        return Response({'message':'no review for that proposal yet!!'})
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET',
    responses={
        200: serializers.AssignmentSerializer,
        401: 'unauthorized'
        
    },
    operation_description='returns a list of assignments for the user making the request'
)
@api_view(['GET'])
def get_my_assignments(request):
    assignments = models.Assignment.objects.filter(reviewer=request.user.id)
    proposals = []
    for assignment in assignments:
        proposal = models.Proposal.objects.get(pk=assignment.proposal.pk)
        ser = serializers.ProposalSerializer(proposal)
        proposals.append(ser.data)
    # 
    if len(proposals)>1:
        return Response(proposals,status=status.HTTP_200_OK)
    return Response({"message":"No Assignments"},status=status.HTTP_404_NOT_FOUND)

    # serializer = serializers.AssignmentSerializer(assignments,many=True)
    # if serializer.data:
    #     return Response(serializer.data)
    # return Response({'message':'You have no assignemnts at the moment!!'})


@swagger_auto_schema(
    method='POST',
    request_body=serializers.ReviewSerializer,
    operation_description='adds a review to the proposal'
)
@api_view(['POST'])
def add_review(request,id):
    data = request.data
    data['reviewer'] = request.user.id
    data['proposal'] = id
    serializer = serializers.ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)    

@swagger_auto_schema(
    method='POST',
    request_body=serializers.QuestionSeriliazer,   
    operation_description='adds a list of questions to the proposal'
)
@api_view(['POST'])
def createQuestions(request):
    data = request.data
    serializer = serializers.QuestionSeriliazer(data=data,many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@swagger_auto_schema(
    method='POST',
    request_body=serializers.AnswerSerializer,
    operation_description='adds a list of answers to the proposal'
)
@api_view(['POST'])
def add_answers(request):
    data = request.data
    print("data",data)
    serializer = serializers.AnswerSerializer(data=data,many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)
    
@api_view()
def proposal_statistics(request):
    pending_proposals_count = models.Proposal.objects.filter(status = "pending").count()
    approved_proposals_count = models.Proposal.objects.filter(status = "approved").count()
    reviewed_proposals_count = models.Proposal.objects.filter(status = "reviewed").count()
    
    return Response({"approved": approved_proposals_count,"pending": pending_proposals_count,"reviewed":reviewed_proposals_count})

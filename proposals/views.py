from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (ListCreateAPIView,CreateAPIView)

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
 
@api_view(['POST'])
def create_proposal(request):
    """
    creates a proposal with the user making the request

    Args:
        template: a unique id of a template

    Returns:
        _type_: _description_
    """
    data = request.data
    print(data)
    data['proposer'] = request.user.id
    serializer = serializers.ProposalSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_my_proposals(request):
    """
    returns a list of submitted proposals from the user making the request
    """
    proposals = models.Proposal.objects.filter(proposer=request.user.id)
    serializer = serializers.ProposalSerializer(proposals,many=True)
    if serializer.data:
        return Response(serializer.data)
    return Response({'message':'You have no proposals at the moment'})


class AssignmentApiView(CreateAPIView):
    """
    Assigns proposal to reviewers

    parameters:
        proposal: unique id of a proposal,
        reviewer: unique id of a reviewer
    """
    
    serializer_class = serializers.AssignmentSerializer
    queryset = models.Assignment.objects.all()
    
@api_view(['GET'])
def assign_proposal(request):
    cat = request.user.category
    print(cat)
    reviewers = models.User.objects.filter(category=cat).filter(role='reviewer')
    proposals = models.Proposal.objects.filter(template__category = cat)
    proposals_serializer = serializers.ProposalSerializer(proposals,many=True)
    reviewers_serializer = UserDetailsSerializer(reviewers,many=True)
    return Response({
        'proposals':proposals_serializer.data,
        'reviewers':reviewers_serializer.data
    })

class AnswerAPIView(CreateAPIView):
    """
    Creates answers from the list of questions

    Args:
        CreateAPIView (_type_): _description_
    """
    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all
    
@api_view(['GET'])
def view_my_proposal_answers(request,id):
    """
    returns a list of the questions together with the answers that the user has given

    Args:
        request (_type_): _description_
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    proposal = models.Proposal.objects.get(pk=id)
    template = proposal.template
    questions = models.Question.objects.filter(template=template)
    answers = models.Answer.objects.filter(proposal=proposal.pk)
    quiz_serializer = serializers.QuestionSeriliazer(questions,many=True)
    ans_serializer = serializers.AnswerSerializer(answers,many=True)
    # if quiz_serializer.is_valid() and ans_serializer.is_valid():
        
    response = {
        'title': template.title,
        'questions':quiz_serializer.data,
        'answers': ans_serializer.data
    }
    return Response(response)
    # return Response({
    #     'qerrors':quiz_serializer.errors,
    #     'aerrors':ans_serializer.data
    # })
@api_view(['GET'])
def get_questions(request,id):
    """
    returns a list of questions available for the selected template identified by the {id}

    Args:
        id (int): unique id identifying a template

   
    """
    questions = models.Question.objects.filter(template=id)
    serializer = serializers.QuestionSeriliazer(questions,many=True)
    template = models.Template.objects.get(pk=id)
    title = template.title
    res ={
        'title':title,
        'questions':serializer.data
    }
    return Response(res)

@api_view(['GET'])
def get_templates(request,cat):
    """
    return a list of templates from the selected category {cat}

    Args:
        request (_type_): _description_
        cat (str): the name of a category

    Returns:
        _type_: _description_
    """
    templates = models.Template.objects.filter(category=cat)
    serializer = serializers.TemplateSerializer(templates,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_proposal_review(request,id):
    """
    returns the review of a proposal identified by {id}

    Args:
       id (str): unique id identifying a proposal

   
    """
    try:
        
        review = models.Review.objects.get(proposal=id)
        serializer = serializers.ReviewSerializer(review)
    except models.Review.DoesNotExist:
        return Response({'message':'no review for that proposal yet!!'})
    return Response(serializer.data)


@api_view(['GET'])
def get_my_assignments(request):
    """
    Returns a list of proposals asigned to the requesting user

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    assignments = models.Assignment.objects.filter(reviewer=request.user.id)
    serializer = serializers.AssignmentSerializer(assignments,many=True)
    if serializer.data:
        return Response(serializer.data)
    return Response({'message':'You have no assignemnts at the moment!!'})


@api_view(['POST'])
def add_review(request,id):
    """
    Args:
        comment(str): the comment for the review 
        marks(str): the marks awarded to the proposal
        id (int): id of the proposal being reviewed

    Returns:
        _type_: _description_
    """
    data = request.data
    data['reviewer'] = request.user.id
    data['proposal'] = id
    serializer = serializers.ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errrors)    



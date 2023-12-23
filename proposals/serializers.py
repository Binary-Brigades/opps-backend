from rest_framework import serializers
from . import models

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = '__all__'
        
class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proposal
        fields = '__all__'
class QuestionSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'
        
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assignment
        fields = '__all__'
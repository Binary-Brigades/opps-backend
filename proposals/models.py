from django.db import models
from users.models import User,Category


STATUS = [
    ('pending','Pending'),
    ('reviewed','Reviewed'),
    ('approved','Approoved')
]


    
class Template(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Question(models.Model):
    question = models.CharField(max_length=255)
    template = models.ForeignKey(Template,on_delete=models.CASCADE)
    marks = models.IntegerField()
    max_words = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.question
    
class Proposal(models.Model):
    template = models.ForeignKey(Template,on_delete=models.CASCADE)
    proposer = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on =models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS,default='pending')
    # assigned = models.CharField(max_length=20,choices=STATUS,default='pending')
    name = models.CharField(max_length = 255, blank = True)
    assigned = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('template','proposer')
    
    def __str__(self):
       return self.template.title

class Answer(models.Model):
    proposal = models.ForeignKey(Proposal,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.TextField()
    
    class Meta:
        unique_together = ('proposal','question')
        
    def __str__(self) -> str:
        return self.answer
        
class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal,on_delete=models.CASCADE)
    comments = models.CharField(max_length=50)
    marks = models.IntegerField()

    def __str__(self):
        return self.comments
    
class Assignment(models.Model):
    proposal = models.ForeignKey(Proposal,on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('proposal','reviewer')
        

    def __str__(self):
        return f"{self.proposal} {self.reviewer}"
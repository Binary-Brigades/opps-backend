from django.db import models
# from proposals.models import Category

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

USER_ROLES = [
    ('coordinator','Coordinator'),
    ('reviewer','Reviewer'),
    ('admin','Admin'),
    ('proposer','Proposer')
]

class UserManager(BaseUserManager):
    def _create_user(self,username,email,password,role,firstname=None,lastname=None,**extra_fields):
        if not username:
            raise ValueError('Username must be provided')
        email = self.normalize_email(email)
        user = self.model(username=username,lastname=lastname,firstname=firstname,email=email,role=role,is_staff=extra_fields['is_staff'],is_superuser=extra_fields['is_superuser'])
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password,role='admin',**extra_fields)
    
class Category(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=50,unique=True,)
    firstname = models.CharField(max_length=30,null=True,blank=True)
    lastname = models.CharField(max_length=30,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=30)
    role = models.CharField(choices=USER_ROLES,max_length=30,null=True,default='proposer',blank=True)
    is_superuser = models.BooleanField(null=True)
    is_staff = models.BooleanField(null=True)
  
    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email',]
    
    def __str__(self):
        return self.username
    

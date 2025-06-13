from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

# Create your models here.

class QuestionManager(models.Manager):
    def questions_in_order(self):
        return self.order_by('created_at')
    
    def new_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
        return self.order_by('likes_count')

    def questions_by_tag(self, tag):
        return self.filter(tags__name=tag)
    
class AnswerManager(models.Manager):
    def hot_answers(self):
        return self.order_by('likes_count')  
    def new_answers(self):
        return self.order_by('-created_at') 

class Question(models.Model):
    objects = QuestionManager()
    name = models.CharField(max_length=255)
    text = models.TextField(default='')
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT)

    tag = models.ManyToManyField('Tag')
    likes_count = models.PositiveIntegerField(default=0, editable=False)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.id})


class Answer(models.Model):
    objects = AnswerManager()
    text = models.TextField(default='')
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AnswerLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    class Meta:
        unique_together= ["answer", "profile"]

    def __str__(self):
        return f"Like #{self.id} on Answer #{self.answer.id}"

class QuestionLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        unique_together= ["question", "profile"]

    def __str__(self):
        return f"Like #{self.id} on Question #{self.question.id}"
    

class Profile(models.Model):
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.nickname or self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, nickname=instance.username)
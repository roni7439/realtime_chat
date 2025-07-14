from django.db import models
from django.contrib.auth.models import User

class ChatGroup(models.Model):
    group_name=models.CharField(max_length=120,unique=True)
    
    def __str__(self):
        return self.group_name
    
    
class GroupMassage(models.Model):
    group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE,related_name='chat_massages')
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username}:{self.body}' 
    
    class Meta:
        ordering=['-created']
        
class PrivetMassage(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender_massage')
    receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciver_massage')
    body=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver} : {self.body[:20]}"
    
      
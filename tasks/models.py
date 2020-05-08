from django.db import models
from org.models import Org
from users.models import User
# Create your models here.
class Task(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    social_media_platform = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    share_link = models.CharField( max_length=30)
    share_text = models.CharField(max_length=65536)
    share_img = models.ImageField( upload_to='uploads/tasks/share_img', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.org} - {self.social_media_platform} - {self.id}"

class Proof(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    screenshot = models.ImageField( upload_to='uploads/tasks/screenshots', null=False)
    points = models.IntegerField()
    proof_status_choices = (
        ('accepted','Accepted'),
        ('pending','Review Pending'),
        ('rejected','Rejected')
    )
    review_by_ai = models.CharField(max_length=50,choices = proof_status_choices)
    review_by_human = models.CharField(max_length=50,choices = proof_status_choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.org} - {self.task.id} -- {self.id}"

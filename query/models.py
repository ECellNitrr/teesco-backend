from django.db import models
from users.models import User
from org.models import Org

# Create your models here.

class QueryRoom(models.Model):
    org = models.ForeignKey(Org,on_delete=models.CASCADE)
    for_user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}-{self.org.name}-{self.for_user.username}'

class Query(models.Model):
    author =  models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length = 65536) 
    query_room = models.ForeignKey(QueryRoom,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}-{self.query_room.id}-{self.author.username}'
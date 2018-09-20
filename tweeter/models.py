import datetime
from django.db import models

# Create your models here.


class Tweet(models.Model):
    """
    Represents a DB entry for Tweets.
    """

    author = models.CharField(max_length=200)
    content = models.CharField(max_length=50)
    created_on = models.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return "{}: {}".format(self.author, self.content)


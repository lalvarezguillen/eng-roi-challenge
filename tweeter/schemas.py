from rest_framework import serializers
from .models import Tweet


class TweetSchema(serializers.Serializer):
    """
    Handles serializing, deserializing and validating Tweets
    """

    author = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=50)
    created_on = serializers.DateTimeField(
        required=False, format="%Y/%m/%d %H:%M:%S"
    )


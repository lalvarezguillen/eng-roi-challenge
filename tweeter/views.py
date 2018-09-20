from io import BytesIO
import logging
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from .models import Tweet
from .schemas import TweetSchema


# The challenge's documentation states that all the functionality
# should be served by the '/' endpoint. So we'll use this
# proto-handler to pass requests to 3 handlers, based on the
# request's method and Content-Type.
def handle_root(request):
    if request.method == "POST":
        return handle_post_tweet(request)

    accept = request.META.get("HTTP_ACCEPT")
    if "text/html" in accept:
        return handle_render_landing(request)
    return handle_get_tweets(request)


def handle_render_landing(request):
    """
    Renders the website's landing page
    """
    return render(request, "tweeter/index.html")


def handle_get_tweets(request):
    """
    Returns a list of the existing Tweets, as JSON.
    """
    tweets = Tweet.objects.order_by("-created_on")
    serialized = TweetSchema(tweets, many=True)
    return JsonResponse(serialized.data, safe=False)


def handle_post_tweet(request):
    """
    Deals with creating new Tweets
    """
    payload = BytesIO(request.body)
    try:
        json_data = JSONParser().parse(payload)
    except ParseError as err:
        logging.error(err)
        return HttpResponse("error", status=400)

    parsed_data = TweetSchema(data=json_data)
    if not parsed_data.is_valid():
        return HttpResponse(json.dumps(parsed_data.errors), status=400)
    tweet = Tweet(**parsed_data.data)
    tweet.save()
    return HttpResponse("asd", status=201)

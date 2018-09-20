import datetime
import json
from unittest import mock
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
import tweeter
from tweeter.views import (
    handle_root,
    handle_render_landing,
    handle_get_tweets,
    handle_post_tweet,
)
from tweeter.models import Tweet


@mock.patch("tweeter.views.handle_render_landing")
@mock.patch("tweeter.views.handle_get_tweets")
@mock.patch("tweeter.views.handle_post_tweet")
class TestHandleRoot(TestCase):
    def setup(self, *_):
        self.client = Client()

    def test_accept_html(
        self, mocked_post_tweet, mocked_get_tweets, mocked_render
    ):
        mocked_render.return_value = HttpResponse()

        header = {"HTTP_ACCEPT": "text/html"}
        self.client.get("/", **header)
        assert not mocked_post_tweet.called
        assert not mocked_get_tweets.called
        assert mocked_render.called

    def test_accept_json(
        self, mocked_post_tweet, mocked_get_tweets, mocked_render
    ):
        mocked_get_tweets.return_value = HttpResponse()

        header = {"HTTP_ACCEPT": "application/json"}
        self.client.get("/", **header)
        assert not mocked_post_tweet.called
        assert mocked_get_tweets.called
        assert not mocked_render.called

    def test_post(self, mocked_post_tweet, mocked_get_tweets, mocked_render):
        mocked_post_tweet.return_value = HttpResponse()

        self.client.post("/")
        assert mocked_post_tweet.called
        assert not mocked_get_tweets.called
        assert not mocked_render.called


class TestRenderLanding(TestCase):
    def test_works(self):
        client = Client()
        headers = {"HTTP_ACCEPT": "text/html"}
        resp = client.get("/", **headers)
        assert resp.status_code == 200


class TestListTweets(TestCase):
    def setup(self):
        self.client = Client()

    def test_lists_all_tweets(self):
        first_tweet = Tweet(
            author="Shaggy",
            content="Scooby Doo where are you?",
            created_on=datetime.datetime(2018, 9, 19),
        )
        first_tweet.save()

        last_tweet = Tweet(
            author="Scooby Doo",
            content="I'm here",
            created_on=datetime.datetime(2018, 9, 20),
        )
        last_tweet.save()

        headers = {"HTTP_ACCEPT": "application/json"}
        resp = self.client.get("/", **headers)
        assert resp.status_code == 200

        tweets = resp.json()
        assert len(tweets) == 2
        assert tweets[0]["created_on"] > tweets[1]["created_on"]

    def test_no_tweets_to_list(self):
        headers = {"HTTP_ACCEPT": "application/json"}
        resp = self.client.get("/", **headers)
        assert resp.status_code == 200

        tweets = resp.json()
        assert not tweets


class TestPostTweet(TestCase):
    def setup(self):
        self.client = Client()

    def test_tweets_are_created(self):
        payload = {"author": "Shaggy", "content": "Scooby Doo where are you?"}
        resp = self.client.post(
            "/", data=payload, content_type="application/json"
        )
        assert resp.status_code == 201

        db_entries = list(Tweet.objects.all())
        assert len(db_entries) == 1

    def test_payload_missing_attributes(self):
        payload = {"author": "Scooby Doo"}
        resp = self.client.post(
            "/", data=payload, content_type="application/json"
        )
        assert resp.status_code == 400

    def test_malformed_payload(self):
        payload = ["this", "is", "sparta"]
        resp = self.client.post(
            "/", data=payload, content_type="application/json"
        )
        assert resp.status_code == 400

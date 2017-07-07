# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from rest_framework import status

from tests import factories as f
from tests.unit.base import BaseAPITestCase


class CommentAPITest(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.restaurant = f.RestaurantFactory(lat=23.11122, lon=-2343.222)
        self.review = f.ReviewFactory(
            restaurant=self.restaurant, user=self.user.profile
        )
        self.comment_post_url = reverse(
            'comment-create', args=(self.review.pk,)
        )
        self.comment_payload = {
            'text': 'This is dummy comment.',
            'user': self.user.profile.id,
            'review': self.review.pk
        }

    def test_comment_creation_for_anonymous_user(self):
        self.comment_payload['user'] = self.anonymous_user
        response = self.client.post(self.comment_post_url, self.comment_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_creation_for_authenticated_user(self):
        self._login()
        response = self.client.post(self.comment_post_url, self.comment_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        pass

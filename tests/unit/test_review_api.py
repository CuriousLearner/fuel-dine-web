# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from rest_framework import status

from tests import factories as f
from tests.unit.base import BaseAPITestCase


class ReviewAPITest(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.restaurant = f.RestaurantFactory(lat=23.11122, lon=-2343.222)
        self.review_post_url = reverse(
            'review-create', args=(self.restaurant.id,)
        )
        self.review_payload = {
            'text': 'This is dummy review',
            'user': self.user.profile.id,
            'restaurant': self.restaurant.id
        }

    def test_review_creation_for_anonymous_user(self):
        self.review_payload['user'] = self.anonymous_user
        response = self.client.post(self.review_post_url, self.review_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_creation_for_authenticated_user(self):
        self._login()
        response = self.client.post(self.review_post_url, self.review_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        pass

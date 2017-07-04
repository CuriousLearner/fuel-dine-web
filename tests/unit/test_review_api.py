# -*- coding: utf-8 -*-

from tests import factories as f
from tests.unit.base import BaseAPITestCase


class ReviewAPITest(BaseAPITestCase):

    def setUp(self):
        self.restaurant = f.RestaurantFactory(lat=23.11122, lon=-2343.222)

    def test_review_posting_for_anonymous_user(self):
        pass

    def test_review_posting_for_authenticated_user(self):
        pass

    def tearDown(self):
        pass

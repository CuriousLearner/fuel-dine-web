# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from rest_framework import status

from tests import factories as f
from tests.unit.base import BaseAPITestCase


class RestaurantAPITest(BaseAPITestCase):
    """Includes following tests for both authenticated and anonymous users:

        - Restaurant Creation
        - Restaurant Listing
        - Restaurant Voting API
        - Restaurant Thumb Down API
        - Restaurant Visited API
    """

    def setUp(self):
        super().setUp()
        self.restaurant = f.RestaurantFactory(lat=23.11122, lon=-2343.222)
        self.restaurant_create_or_listing_url = reverse('restaurant-create-list')
        self.restaurant_detail_url = reverse(
            'restaurant-detail', args=(self.restaurant.id,)
        )

        self.restaurant_payload = {
            'name': 'Sagar Ratna',
            'lat': '23.37483',
            'lon': '-483.3245',
            'address': 'South Delhi'
        }

        self.restaurant_vote_up_url = reverse(
            'restaurant-vote', args=(self.restaurant.id, 'up')
        )

        self.restaurant_vote_down_url = reverse(
            'restaurant-vote', args=(self.restaurant.id, 'down')
        )

        self.restaurant_thumbdown_url = reverse(
            'restaurant-thumbdown', args=(self.restaurant.id,)
        )

        self.restaurant_visited_url = reverse(
            'restaurant-visited', args=(self.restaurant.id,)
        )

    def test_restaurant_listing_for_anonymous_user(self):
        response = self.client.get(self.restaurant_create_or_listing_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_listing_for_authenticated_user(self):
        self._login()
        response = self.client.get(self.restaurant_create_or_listing_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_details_for_anonymous_user(self):
        response = self.client.get(self.restaurant_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_details_for_authenticated_user(self):
        self._login()
        response = self.client.get(self.restaurant_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_creation_for_anonymous_user(self):
        self.restaurant_payload['user'] = self.anonymous_user
        response = self.client.post(
            self.restaurant_create_or_listing_url, self.restaurant_payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_creation_for_authenticated_user(self):
        self._login()
        response = self.client.post(
            self.restaurant_create_or_listing_url, self.restaurant_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_restaurant_creation_without_address_or_name(self):
        self._login()

        # Try to create restaurant without address
        address = self.restaurant_payload.pop('address')
        response = self.client.post(
            self.restaurant_create_or_listing_url, self.restaurant_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to create restaurant without name
        self.restaurant_payload['address'] = address
        self.restaurant_payload.pop('name')
        response = self.client.post(
            self.restaurant_create_or_listing_url, self.restaurant_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_restaurant_creation_without_latitude_or_longitude(self):
        self._login()

        # Try to create restaurant without latitude `lat`
        latitude = self.restaurant_payload.pop('lat')
        response = self.client.post(
            self.restaurant_create_or_listing_url, self.restaurant_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try to create restaurant without longitude `lon`
        self.restaurant_payload['lat'] = latitude
        self.restaurant_payload.pop('lon')
        response = self.client.post(
            self.restaurant_create_or_listing_url, self.restaurant_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_vote_up_for_anoymous_user(self):
        response = self.client.post(self.restaurant_vote_up_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_vote_up_for_authenticated_user(self):
        self._login()
        response = self.client.post(self.restaurant_vote_up_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_vote_down_for_anonymous_user(self):
        response = self.client.post(self.restaurant_vote_down_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_vote_down_for_authenticated_user(self):
        self._login()
        response = self.client.post(self.restaurant_vote_down_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_thumb_down_for_anonymous_user(self):
        response = self.client.post(self.restaurant_thumbdown_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_thumb_down_for_authenticated_user(self):
        self._login()
        response = self.client.post(self.restaurant_thumbdown_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_visited_for_anonymous_user(self):
        response = self.client.post(self.restaurant_visited_url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_restaurant_visited_for_authenticated_user(self):
        self._login()
        response = self.client.post(self.restaurant_visited_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_repeated_restaurant_visit_by_same_user(self):
        self._login()
        response = self.client.post(self.restaurant_visited_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.restaurant_visited_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_repeated_restaurant_vote_up_by_same_user(self):
        self._login()
        response = self.client.post(self.restaurant_vote_up_url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.restaurant_vote_up_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.restaurant.delete()

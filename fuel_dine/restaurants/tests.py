# -*- coding: utf-8 -*-

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from fuel_dine.users.models import User
from .models import Restaurant, Review


class APITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@localhost.com", password="test@localhost"
        )
        self.restaurant = Restaurant.objects.create(
            name="Sagar Ratna", lat=17.388822, lon=-293.2333, is_active=True
        )

        self.review = Review.objects.create(
            restaurant=self.restaurant, text="Awesome food!",
            user=self.user.profile
        )

    def test_restaurant(self):
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertIn("Sagar Ratna", self.restaurant.name)

    def tearDown(self):
        self.user.delete()
        self.restaurant.delete()
        self.review.delete()


class RestaurantTest(APITestCase):
    def test_create_restaurant(self):
        url = reverse('account-list')
        data = {
            'name': 'Sagar Ratna',
            'lon': 23.111134,
            'lat': -23.222245
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'Sagar Ratna')

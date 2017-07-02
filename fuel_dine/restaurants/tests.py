# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
rom rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory


def TestRestaurant(TestCase):

    def setUp(self):
        pass


    def test_dummy(self):
        # Create a JSON POST request
        factory = APIRequestFactory()
        request = factory.post('/notes/', {'title': 'new idea'}, format='json')


    def tearDown(self):
        pass



# Create a JSON POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'}, format='json')


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')

from django.test import TestCase


class FooTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def this_wont_run(self):
        print 'Fail'

    def test_this_will(self):
        print 'Win'

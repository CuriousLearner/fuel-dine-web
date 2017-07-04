# -*- coding: utf-8 -*-

from django.test import TestCase

# Related third party imports
from rest_framework.test import APIClient

# fuel_dine imports
from ..factories import UserFactory


class BaseAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.anonymous_user = UserFactory()
        self.user = UserFactory.create(email='f@F.com', password='123456')

    def _login(self):
        self.client.login(email=self.user.username, password='123456')

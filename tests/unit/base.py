# -*- coding: utf-8 -*-

from django.test import TestCase

# Related third party imports
from rest_framework.test import APIClient

# fuel_dine imports
from ..factories import create_user, UserFactory


class BaseAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.anonymous_user = UserFactory()
        self.user = create_user(email='test@localhost.com', password='123456')

    def _login(self):
        self.client.login(email=self.user.email, password='123456')

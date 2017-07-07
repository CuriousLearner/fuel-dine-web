# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from rest_framework import status

from tests.unit.base import BaseAPITestCase


class RestaurantAPITest(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.get_current_user_mail_api = reverse('who-am-i')

    def test_who_am_I_for_authenticated_user(self):
        self._login()
        response = self.client.get(self.get_current_user_mail_api, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'email': self.user.email}
        )

    def test_who_am_I_for_anonymous_user(self):
        response = self.client.get(self.get_current_user_mail_api, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        pass

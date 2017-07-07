# -*- coding: utf-8 -*-

# Third Party Stuff
import pytest

from django.core.urlresolvers import reverse
from rest_framework import status

from fuel_dine.restaurants.models import Restaurant

pytestmark = pytest.mark.django_db


def test_root_txt_files(client):
    files = ['robots.txt', 'humans.txt']
    for filename in files:
        url = reverse('root-txt-files', kwargs={'filename': filename})
        response = client.get(url)
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/plain'


def test_landing_pages(client):
    # Test that these urls are rendered properly and doesn't required authorization
    urls = [
        '/about/',
        '/',
    ]
    for url in urls:
        response = client.get(url)
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/html; charset=utf-8'
        assert '</body>' in response.content.decode('utf-8')


def test_blank_home_page(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'There are no restaurants to display.' in response.content.decode('utf-8')

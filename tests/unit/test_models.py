# -*- coding: utf-8 -*-

import pytest

from tests import factories as f


@pytest.mark.parametrize('method', [
    'get_votes_count',
    '__str__'
])
def test_restaurant_model_method_works(db, method):
    restaurant = f.RestaurantFactory(lat=23.2223443, lon=-243.222334)
    assert getattr(restaurant, method)


@pytest.mark.parametrize('method', [
    '__str__',
])
def test_visit_model_method_works(db, method):
    user = f.UserFactory(email='f@F.com', password='12345453')
    restaurant = f.RestaurantFactory(lat=23.2223443, lon=-243.222334)
    visit = f.VisitFactory(user=user.profile, restaurant=restaurant)
    assert getattr(visit, method)


@pytest.mark.parametrize('method', [
    '__str__',
])
def test_review_model_method_works(db, method):
    user = f.UserFactory(email='f@F.com', password='12345453')
    restaurant = f.RestaurantFactory(lat=23.2223443, lon=-243.222334)
    review = f.ReviewFactory(restaurant=restaurant, user=user.profile)
    assert getattr(review, method)


@pytest.mark.parametrize('method', [
    '__str__',
])
def test_comment_model_method_works(db, method):
    user = f.UserFactory(email='f@F.com', password='12345453')
    restaurant = f.RestaurantFactory(lat=23.2223443, lon=-243.222334)
    review = f.ReviewFactory(restaurant=restaurant, user=user.profile)
    comment = f.CommentFactory(review=review, user=user.profile)
    assert getattr(comment, method)

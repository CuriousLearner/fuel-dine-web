# -*- coding: utf-8 -*-
"""
Helpers to create dynamic model instances for testing purposes.

Usages:
>>> from tests import factories as f
>>>
>>> user = f.create_user(first_name="Robert", last_name="Downey")  # creates single instance of user
>>> users = f.create_user(n=5, is_active=False)  # creates 5 instances of user

There is a bit of magic going on behind the scenes with `G` method from https://django-dynamic-fixture.readthedocs.io/
"""

# Third Party Stuff
import factory

from django.apps import apps
from django.conf import settings
from django_dynamic_fixture import G


def create_user(**kwargs):
    """Create an user along with their dependencies."""
    User = apps.get_model(settings.AUTH_USER_MODEL)
    user = G(User, **kwargs)
    user.set_password(kwargs.get('password', 'test'))
    user.save()
    return user


class Factory(factory.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True


class UserFactory(Factory):
    class Meta:
        model = "users.User"
        strategy = factory.CREATE_STRATEGY


class ProfileFactory(Factory):
    class Meta:
        model = "users.Profile"
        strategy = factory.CREATE_STRATEGY


class RestaurantFactory(Factory):
    class Meta:
        model = "restaurants.Restaurant"
        strategy = factory.CREATE_STRATEGY


class VisitFactory(Factory):
    class Meta:
        model = "restaurants.Visit"
        strategy = factory.CREATE_STRATEGY


class CommentFactory(Factory):
    class Meta:
        model = "restaurants.Comment"
        strategy = factory.CREATE_STRATEGY


class ReviewFactory(Factory):
    class Meta:
        model = "restaurants.Review"
        strategy = factory.CREATE_STRATEGY

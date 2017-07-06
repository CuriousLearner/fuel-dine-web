# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Restaurant, ThumbDown, Visit
from .serializers import (
    RestaurantSerializer, ReviewSerializer, CommentSerializer,
    ReviewPOSTSerializer, CommentPOSTSerializer
)


class RestaurantView(ListCreateAPIView):
    """Restaurant Listing and creating Restaurant resource.
    """
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)


class ReviewView(CreateAPIView):
    """API for creating reviews for restaurants.
    """
    queryset = ReviewSerializer
    serializer_class = ReviewPOSTSerializer


class CommentView(CreateAPIView):
    """API for posting comments on reviews.
    """
    queryset = CommentSerializer
    serializer_class = CommentPOSTSerializer


class RestaurantGeocodingTemplate(TemplateView):
    template_name = 'restaurants/add_restaurant_geocoding.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['js_file_name'] = 'geocode.js'
        context['GOOGLE_SERVICES_API_KEY'] = settings.GOOGLE_SERVICES_API_KEY
        return context


class RestaurantReverseGeocodingTemplate(TemplateView):
    template_name = 'restaurants/add_restaurant_geocoding_reverse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['js_file_name'] = 'reverse_geocode.js'
        context['GOOGLE_SERVICES_API_KEY'] = settings.GOOGLE_SERVICES_API_KEY
        return context


class RestaurantDetailView(RetrieveAPIView):
    """Restaurant Detail API to be displayed on Restaurant Display page
    along with reviews and comments.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def vote_for_restaurant(request, pk, action):
    """API for up vote or down vote a particular Restaurant.

    :param request: HttpRequest Object.
    :param pk: Primary key of Restaurant.
    :param action: either `up` for up voting or `down` for down voting the
    restaurant.
    :return: Return 201 status on successful vote cast & JSON Response as:
    {
        'data': 'Vote casted successfully'
    }

    Return 400 status on Unknown action & JSON Response as:
    {
        'error': 'Unknown action for casting vote'
    }
    """
    user_id = request.user.profile.id
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist:
        return Response(
            data={'error': 'Restaurant does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    vote_casted = False

    if restaurant.votes.exists(user_id):
        return Response(
            data={'error': 'You have casted vote before for this restaurant'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if action == 'up':
        restaurant.votes.up(user_id=user_id)
        vote_casted = True
    elif action == 'down':
        restaurant.votes.down(user_id=user_id)
        vote_casted = True

    if vote_casted:
        return Response(
            data={'data': 'Vote casted successfully'},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            data={'error': 'Unknown action for casting vote'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def thumbs_down_for_restaurant(request, pk):
    """API for thumbs down for a particular Restaurant.

    :param request: HttpRequest Object.
    :param pk: Primary key of Restaurant.
    :return: Return 201 status on successful vote cast & JSON Response as:
    {
        'data': 'Restaurant thumbs down successfully'
    }
    Return 400 status on Unknown action & JSON Response as:
    {
        'error': 'Restaurant already thumbs down by you'
    }
    """
    user = request.user.profile
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist:
        return Response(
            data={'error': 'Restaurant does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    # Try getting a thumb down if it exists or create one and return
    # appropriate response based on value of `created`.
    thumb_down, created = ThumbDown.objects.get_or_create(restaurant=restaurant, user=user)
    if created:
        return Response(
            data={'data': 'Restaurant thumbs down successfully'},
            status=status.HTTP_201_CREATED
        )

    return Response(
        data={'error': 'Restaurant already thumbs down by you'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def mark_restaurant_visited(request, pk):
    """API for marking restaurant visited for the user.

    :param request: HttpRequest Object.
    :param pk: Primary key of Restaurant.
    :return: Return 201 status on successful vote cast & JSON Response as:
    {
        'data': 'Visit marked successfully for this restaurant'
    }

    Return 400 status on Unknown action & JSON Response as:
    {
        'error': 'Visit already marked for this restaurant'
    }
    """
    user = request.user.profile
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist:
        return Response(
            data={'error': 'Restaurant does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    # Try getting a visit if it exists or create one and return appropriate
    # response based on value of `created`.
    visit, created = Visit.objects.get_or_create(restaurant=restaurant, user=user)
    if created:
        return Response(
            data={'data': 'Visit marked successfully for this restaurant'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        data={'error': 'Visit already marked for this restaurant'},
        status=status.HTTP_400_BAD_REQUEST
    )

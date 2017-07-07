# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.conf import settings

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, ListCreateAPIView, RetrieveAPIView
)
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Restaurant, ThumbDown, Visit
from .serializers import (
    RestaurantSerializer, ReviewSerializer, CommentSerializer
)


class RestaurantView(ListCreateAPIView):
    """Restaurant Listing and creating Restaurant resource.
    Listing
    """
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        # Do not display restaurants to user that are thumbs down by them.
        qs = ThumbDown.objects.filter(user=self.request.user.profile.id)
        restaurant_thumbdown_list = list(qs.values_list('restaurant', flat=True))

        return Restaurant.objects.filter(
            is_active=True
        ).exclude(id__in=restaurant_thumbdown_list)


class ReviewView(CreateAPIView):
    """API for creating reviews for restaurants.
    """
    serializer_class = ReviewSerializer


class CommentView(CreateAPIView):
    """API for posting comments on reviews.
    """
    serializer_class = CommentSerializer


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


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def who_am_i(request):
    """API for returning the email of current user. This is for the
    requirement of displaying special symbol with review that are posted by
    the current logged in user.

    :param request: HttpRequest Object.
    """
    email = request.user.email
    return Response(
        data={'email': email},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def select_restaurant_for_dining_based_on_votes(request):
    """Get top voted restaurants to choose among the best restaurants for
    dining.

    :param request: HttpRequest Object.
    """
    restaurant_id_list = list(
        ThumbDown.objects.all().values_list('restaurant', flat=True)
    )
    restaurants = Restaurant.objects.all()\
        .exclude(id__in=restaurant_id_list).order_by('-vote_score')
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(
        data={'result': serializer.data},
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
@renderer_classes((JSONRenderer,))
def reset_vote_count_for_restaurants(request):
    """Reset vote count for all restaurants done by current user to choose a
    new restaurant next time for dining.

    :param request: HttpRequest Object.
    """
    # TODO: Move this task to be asynchronous via Celery.
    # TODO: Enable resetting votes for all users in all restaurants.
    restaurants = Restaurant.objects.all()
    restaurants.update(num_vote_up=0, num_vote_down=0, vote_score=0)
    user = request.user
    for restaurant in restaurants:
        restaurant.votes.delete(user_id=None)
    return Response(
        data={'result': "Votes reset successfully!"},
        status=status.HTTP_200_OK
    )

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView


from .models import Restaurant, Review, Comment, ThumbDown, Visit
from .serializers import (
    RestaurantSerializer, ReviewSerializer, CommentSerializer,
    ReviewWithTextSerializer, CommentWithTextSerializer,
    RestaurantFormSerializer
)

# Create your views here.


class RestaurantView(ListAPIView):
    """Restaurant Listing API for home page.

    Renders restaurants/index.html by default. Also support JSON serialization.
    """
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    template_name = "restaurants/index.html"


class AddRestaurantView(APIView):
    """APIView for reading and adding a new restaurant instance.

    Default TemplateHTMLRenderer would render form for adding restaurant.

    The template uses forms support for adding restaurant via geolocating or
    reverse geolocating.
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'restaurants/add_restaurant_geocoding.html'

    def get(self, request):
        serializer = RestaurantFormSerializer()
        if request.get_full_path() == reverse('restaurant-add-geo'):
            js_file_name = 'geocode.js'
        else:
            js_file_name = 'reverse_geocode.js'

        return Response({
            'serializer': serializer,
            'js_file_name': js_file_name,
            'GOOGLE_SERVICES_API_KEY': settings.GOOGLE_SERVICES_API_KEY
        })

    def post(self, request):
        serializer = RestaurantFormSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'serializer': serializer}
            )
        serializer.save()
        return redirect('thanks')


class AddReviewView(APIView):
    """APIView for reading and adding a new review instance.

    Default TemplateHTMLRenderer would render form for adding review to a
    particular restaurant.
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'restaurants/add_review_form.html'

    def get(self, request, pk):
        serializer = ReviewWithTextSerializer()
        return Response({'serializer': serializer, 'restaurant': pk})

    def post(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        data = dict(request.data)
        data['text'] = data['text'][0]
        data['restaurant'] = restaurant.pk
        data['user'] = request.user.profile.pk
        serializer = ReviewSerializer(data=data)
        if not serializer.is_valid():
            serializer = ReviewWithTextSerializer()
            return Response(
                {'serializer': serializer, 'restaurant': pk}
            )
        serializer.save()
        return redirect('thanks')


class AddCommentView(APIView):
    """APIView for reading and adding a new review instance.

    Default TemplateHTMLRenderer would render form for adding comment to a
    particular review..
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'restaurants/add_comment_form.html'

    def get(self, request, pk):
        serializer = CommentWithTextSerializer()
        return Response({'serializer': serializer, 'review': pk})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        data = dict(request.data)
        data['text'] = data['text'][0]
        data['review'] = review.pk
        data['user'] = request.user.profile.pk
        serializer = CommentSerializer(data=data)
        if not serializer.is_valid():
            serializer = CommentWithTextSerializer()
            return Response(
                {'serializer': serializer, 'review': pk}
            )
        serializer.save()
        return redirect('thanks')


class ReviewView(ListAPIView):
    """Review Listing API
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class RestaurantDetailView(DetailView):
    """Restaurant Detail API to be displayed on Restaurant Display page
    along with reviews and comments.
    """
    model = Restaurant
    permission_classes = (IsAuthenticated,)


class RestaurantCreateView(CreateAPIView):
    """API to create restaurant
    """
    model = Restaurant
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)


class ReviewCreateView(CreateAPIView):
    """API to post new Reviews for Restaurants
    """
    model = Review
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class CommentCreateView(CreateAPIView):
    """API to post new comments on Reviews
    """
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)


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

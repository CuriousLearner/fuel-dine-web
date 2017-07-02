# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Restaurant, Review, Comment
from .serializers import RestaurantSerializer, ReviewSerializer, CommentSerializer

# Create your views here.


class RestaurantView(ListCreateAPIView):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    template_name = "restaurants/index.html"


class ReviewView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class RestaurantDetailView(DetailView):
    model = Restaurant


class RestaurantCreateView(CreateAPIView):
    model = Restaurant
    serializer_class = RestaurantSerializer


class ReviewCreateView(CreateAPIView):
    model = Review
    serializer_class = ReviewSerializer


class CommentCreateView(CreateAPIView):
    model = Comment
    serializer_class = CommentSerializer


# All FBVs goes here


@api_view(['POST'])
def vote_for_restaurant(request, pk, action):
    user_id = request.user.profile.id
    try:
        restaurant = Restaurant.objects.get(id=pk)
    except Restaurant.DoesNotExist:
        return Response(
            data={'error': 'Restaurant does not exist'},
            status=status.HTTP_404_NOT_FOUND
        )
    vote_casted = False
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


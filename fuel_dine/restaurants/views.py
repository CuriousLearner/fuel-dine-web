# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Restaurant, Review, Comment
from .serializers import RestaurantSerializer, ReviewSerializer, CommentSerializer
from .forms import ReviewForm, CommentForm

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

def add_review_form(request, pk):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReviewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            review = form.save(commit=False)
            review.user = request.user.profile
            review.restaurant = Restaurant.objects.get(pk=pk)
            review.save()
            messages.success(request, "Thanks for filling up the review!")
            return HttpResponseRedirect('/thanks/')

    else:
        form = ReviewForm(initial={
            'text': 'I like...'
        })

    return render(request, 'restaurants/add_review_form.html',
                  {'form': form, 'restaurant': pk})


def add_comment_form(request, pk):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            comment = form.save(commit=False)
            comment.user = request.user.profile
            comment.review = Review.objects.get(pk=pk)
            comment.save()
            messages.success(request, "Thanks for filling up the comment!")
            return HttpResponseRedirect('/thanks/')

    else:
        form = CommentForm(initial={
            'text': 'I like...'
        })

    return render(request, 'restaurants/add_comment_form.html',
                  {'form': form, 'review': pk})


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


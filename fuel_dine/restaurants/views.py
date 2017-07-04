# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from .models import Restaurant, Review, Comment
from .serializers import RestaurantSerializer, ReviewSerializer, CommentSerializer
from .forms import ReviewForm, CommentForm, RestaurantForm

# Create your views here.


class RestaurantView(ListCreateAPIView):
    """Restaurant Listing API for home page.

    Renders restaurants/index.html by default. Also support JSON serialization.
    """
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    template_name = "restaurants/index.html"


class ReviewView(ListCreateAPIView):
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


# All FBVs goes here

@login_required()
@permission_classes(IsAuthenticated,)
def add_review_form(request, pk):
    """View for rendering form for adding review to a particular restaurant.
    Initial form contains Review text as "I like ..."

    :param request: HTTPRequest Object
    :param pk: Primary key of Restaurant to post review about.
    :return: HttpResponseRedirect to /thanks/ on successful posting.
    If Review text is empty, return the Form with error.
    """
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


@api_view(['GET', 'POST'])
@permission_classes(IsAuthenticated,)
def add_comment_form(request, pk):
    """View for rendering form for adding comment to a particular review.
    Initial form contains Comment text as "I like ..."

    :param request: HTTPRequest Object
    :param pk: Primary key of Review object to post comment about.
    :return: HttpResponseRedirect to /thanks/ on successful posting.
    If Comment text is empty, return the Form with error.
    """
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


@api_view(['GET', 'POST'])
def add_restaurant_form(request):
    """View for rendering form for adding restaurant.

    Dynamically attaches context of rendering geo-location searching or reverse
    geo-location searching of the restaurant.

    The context would consist of template and js file to be chosen to render
    the view.

    :param request: HTTPRequest Object
    :return: HttpResponseRedirect to /thanks/ on successful posting.
    If Comment text is empty, return the Form with error.
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RestaurantForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            restaurant = form.save(commit=False)
            restaurant.save()
            messages.success(request, "Thanks for adding the restaurant!")
            return HttpResponseRedirect('/thanks/')

    else:
        form = RestaurantForm()

    context = {
        'form': form,
        'GOOGLE_SERVICES_API_KEY': settings.GOOGLE_SERVICES_API_KEY
    }

    if request.get_full_path() == reverse('restaurant-add-geo'):
        template_name = 'restaurants/add_restaurant_geocoding.html'
        context['js_file_name'] = 'geocode.js'
    else:
        template_name = 'restaurants/add_restaurant_geocoding_reverse.html'
        context['js_file_name'] = 'reverse_geocode.js'

    return render(request, template_name, context)


@api_view(['POST'])
@permission_classes(IsAuthenticated,)
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


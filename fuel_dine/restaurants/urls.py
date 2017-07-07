# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [

    # APIs exposed

    url(r'^api/restaurant/$', views.RestaurantView.as_view(),
        name='restaurant-create-list'),

    url(r'^api/restaurant/(?P<pk>\d+)/$',
        views.RestaurantDetailView.as_view(),
        name='restaurant-detail'),

    url(r'^api/restaurant/(?P<pk>\d+)/review/$', views.ReviewView.as_view(),
        name='review-create'),

    url(r'^api/review/(?P<pk>\d+)/comment/$', views.CommentView.as_view(),
        name='comment-create'),

    url(r'^api/restaurant/(?P<pk>\d+)/vote/(?P<action>\w+)/$',
        views.vote_for_restaurant,
        name='comment-create'),

    url(r'^api/restaurant/(?P<pk>\d+)/thumbdown/$',
        views.thumbs_down_for_restaurant,
        name='comment-create'),

    url(r'^api/restaurant/(?P<pk>\d+)/visited/$',
        views.mark_restaurant_visited,
        name='comment-create'),

    url(r'^api/me/$', views.who_am_i,
        name='who-am-i'),

    url(r'^api/votes/reset/$', views.reset_vote_count_for_restaurants,
        name='reset-vote-count'),

    url(r'^api/results/$', views.select_restaurant_for_dining_based_on_votes,
        name='choose-restaurant-for-dining'),

    # Normal Django Templates url go below

    url(r'^add_restaurant_geocoding/$',
        views.RestaurantGeocodingTemplate.as_view(),
        name='restaurant-add-geo'),

    url(r'^add_restaurant_reverse_geocoding/$',
        views.RestaurantReverseGeocodingTemplate.as_view(),
        name='restaurant-add-geo-rev'),

    url(r'^$', TemplateView.as_view(template_name='restaurants/index.html'),
        name='home'),

    url(r'^restaurant/(?P<pk>\d+)/$',
        TemplateView.as_view(template_name='restaurants/restaurant_detail.html'),
        name='restaurant-detail-template'),

    url(r'^restaurant/(?P<pk>\d+)/review/$',
        TemplateView.as_view(template_name='restaurants/add_review_form.html'),
        name='review-add-template'),

    url(r'^review/(?P<pk>\d+)/comment/$',
        TemplateView.as_view(template_name='restaurants/add_comment_form.html'),
        name='comment-add-template'),

]

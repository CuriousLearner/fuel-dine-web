# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/v1/restaurants/$', views.RestaurantView.as_view()),
    url(r'^api/v1/reviews/$', views.ReviewView.as_view()),
]

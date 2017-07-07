# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

# Third party imports
from vote.models import VoteModel

# Local imports of fuel_dine
from fuel_dine.users.models import Profile

# Create your models here.


class Place(models.Model):
    lat = models.FloatField(verbose_name=_(u'latitude'))
    lon = models.FloatField(verbose_name=_(u'longitude'))

    def __str__(self):
        return "Coordinates: {}, {}".format(self.lat, self.lon)

    class Meta:
        abstract = True
        verbose_name = "place"
        verbose_name_plural = "places"


class ReviewComments(models.Model):
    user = models.ForeignKey(Profile, null=False,
                             blank=False, verbose_name=_(u'user'))
    text = models.TextField(null=True, blank=True, verbose_name=_(u'text'))
    posted_at = models.DateTimeField(default=timezone.now, null=False,
                                     blank=False, verbose_name=_(u'posted_at'))

    class Meta:
        abstract = True
        verbose_name = "restaurant"
        verbose_name_plural = "restaurants"


class Restaurant(VoteModel, Place):
    name = models.CharField(max_length=100, verbose_name=_(u'name'))
    is_active = models.BooleanField(default=True, verbose_name=_(u'is_active'))
    description = models.TextField(blank=True, null=True,
                                   verbose_name=_(u'description'))
    website = models.URLField(blank=True, null=True, verbose_name=_(u'website'))
    address = models.TextField(verbose_name='Address',
                               help_text='Location of the restaurant')
    contact = models.CharField(max_length=10, blank=True, null=True,
                               verbose_name=_(u'contact'))
    created_at = models.DateTimeField(default=timezone.now, null=False,
                                      blank=False, verbose_name=_(u'created_at'))

    class Meta:
        verbose_name = "restaurant"
        verbose_name_plural = "restaurants"
        ordering = ['-created_at']

    def __str__(self):
        return "{0}".format(self.name)

    def get_votes_count(self):
        return self.votes.count()


class Visit(models.Model):
    user = models.ForeignKey(Profile, null=False,
                             on_delete=models.CASCADE,
                             blank=False, verbose_name=_(u'user'))
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False,
                                   on_delete=models.CASCADE,
                                   verbose_name=_(u'restaurant'))
    created_at = models.DateTimeField(default=timezone.now, null=False,
                                      blank=False, verbose_name=_(u'created_at'))

    def __str__(self):
        return "{} - {}".format(self.user, self.restaurant)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "visit"
        verbose_name_plural = "visits"


class Review(ReviewComments):
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False,
                                   verbose_name=_(u'restaurant'),
                                   related_name='reviews',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"
        ordering = ['-posted_at']

    def __str__(self):
        return "{0} - {1}".format(self.user, self.text)


class Comment(ReviewComments):
    review = models.ForeignKey(Review, null=False, blank=False,
                               verbose_name=_(u'review'),
                               related_name='comments',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ['-posted_at']

    def __str__(self):
        return "{0} - {1}".format(self.user, self.text)


class ThumbDown(models.Model):
    user = models.ForeignKey(Profile, null=False,
                             blank=False, verbose_name=_(u'user'))
    restaurant = models.ForeignKey(Restaurant, null=False, blank=False,
                                   verbose_name=_(u'restaurant'))
    created_at = models.DateTimeField(default=timezone.now, null=False,
                                      blank=False, verbose_name=_(u'created_at'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = "thumb_down"
        verbose_name_plural = "thumb_downs"

    def __str__(self):
        return "{0} did thumbs down to {1}".format(self.user, self.restaurant)

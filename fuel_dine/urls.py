# -*- coding: utf-8 -*-
"""Root url routering file.

You should put the url config in their respective app putting only a
refernce to them here.
"""

# Third Party Stuff
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# fuel_dine Stuff
from fuel_dine.base import views as base_views

from . import routers, schemas

from fuel_dine.restaurants import views as restaurant_views

handler500 = base_views.server_error

# Top Level Pages
# ==============================================================================
urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'},  name='logout'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    # Your stuff: custom urls go here
    url(r'^$', restaurant_views.RestaurantView.as_view(), name='home'),
    url(r'restaurant/(?P<pk>\d+)$',
        restaurant_views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    url(r'restaurant/(?P<pk>\d+)/vote/(?P<action>\w+)$',
        restaurant_views.vote_for_restaurant, name='restaurant-vote'),
    url(r'restaurant/(?P<pk>\d+)/review/',
        restaurant_views.add_review_form, name='review-add'),
    url(r'review/(?P<pk>\d+)/comment/',
        restaurant_views.add_comment_form, name='comment-add'),
    url(r'thanks/',
        TemplateView.as_view(template_name='pages/thanks.html'),
        name='thanks'),
]

urlpatterns += [

    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        base_views.root_txt_files, name='root-txt-files'),

    # Rest API
    url(r'^api/', include(routers.router.urls)),

    # Django Admin
    url(r'^{}/'.format(settings.DJANGO_ADMIN_URL), admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.API_DEBUG:
    urlpatterns += [
        # Browsable API
        url('^schema/$', schemas.schema_view, name='schema'),
        url(r'^api-playground/$', schemas.swagger_schema_view, name='api-playground'),
        url(r'^api/auth-n/', include('rest_framework.urls', namespace='rest_framework')),
    ]

if settings.DEBUG:
    from django.views import defaults as dj_default_views
    from django.urls import get_callable

    # debug toolbar
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    # Livereloading
    urlpatterns += [url(r'^devrecargar/', include('devrecargar.urls', namespace='devrecargar'))]

    urlpatterns += [
        url(r'^400/$', dj_default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', dj_default_views.permission_denied, kwargs={'exception': Exception('Permission Denied!')}),
        url(r'^403_csrf/$', get_callable(settings.CSRF_FAILURE_VIEW)),
        url(r'^404/$', dj_default_views.page_not_found, kwargs={'exception': Exception('Not Found!')}),
        url(r'^500/$', handler500),
    ]

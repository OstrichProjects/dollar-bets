from django.conf.urls import patterns, include, url
from rest_framework import routers
from bets import views

"""
Simple router for API views from rest_framework
API views are currently at "api/v1/"

"api_auth/" is for rest_framework authentication
"auth/venmo/" is the redirect for the Venmo OAuth
"""

router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'bets',views.BetViewSet)

urlpatterns = patterns('',
	url(r'api/v1/',include(router.urls)),
	url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'auth/venmo/', views.venmoauth, name='venmoauth'),
)
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from api.views import MovieViewSet, RatingViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)


urlpatterns = [
    path('', include(router.urls)),

]

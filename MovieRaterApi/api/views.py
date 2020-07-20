from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Movie, Rating
from api.serializer import MovieSerializer, RatingSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = (MovieSerializer)
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            corresponding_user = request.user
            corresponding_movie = Movie.objects.get(id = pk)
            stars = request.data['stars']

            try:
                rating = Rating.objects.get(user=corresponding_user.id, movie=corresponding_user.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_202_ACCEPTED)
            except:
                rating = Rating.objects.create(user=corresponding_user, movie=corresponding_movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating Created', 'result': serializer.data}
                return Response(response, status=status.HTTP_202_ACCEPTED)

        else:
            return Response('Bad Boy!', status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = (RatingSerializer)
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
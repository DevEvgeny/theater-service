from datetime import datetime

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, mixins, status

from box_office.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket)
from box_office.serializers import (
    ActorSerializer)


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
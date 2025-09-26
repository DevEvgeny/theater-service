from datetime import datetime

from django.db.models import F, Count
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
    ActorSerializer,
    GenreSerializer, TheatreHallSerializer, PerformanceSerializer, PlaySerializer, PlayListSerializer,
    PlayDetailSerializer, ReservationSerializer, PerformanceListSerializer, PerformanceDetailSerializer,
    ReservationListSerializer
)


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Play.objects.prefetch_related("actors", "genres")

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer




class PerformanceViewSet(
    viewsets.ModelViewSet
):
    queryset = (
        Performance.objects.all()
        .select_related("play", "theatre_hall")
        .annotate(
            tickets_available=(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related()
        return queryset


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__performance__play",
                "tickets__performance__theatre_hall")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
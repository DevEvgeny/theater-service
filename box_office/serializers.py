from django.template.defaultfilters import slugify
from rest_framework import serializers

from box_office.models import (
    Play,
    Actor,
    Genre,
    TheatreHall, Performance, Reservation, Ticket
)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity"
        )



class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "descriptions",
            "actors",
            "genres",
        )


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "descriptions",
            "actors",
            "genres",
        )


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "descriptions",
            "actors",
            "genres",
        )


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time",
        )


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(source="theatre_hall.name", read_only=True)
    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "theatre_hall_name",
            "show_time",
        )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "created_at",
            "user"
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "performance",
            "tickets"
        )
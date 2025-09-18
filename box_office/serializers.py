from rest_framework import serializers

from box_office.models import (
    Play,
    Actor,
    Genre,
    TheatreHall, Performance, Reservation
)


class ActorSerializer(serializers.Serializer):
    class Meta:
        model = Actor
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class GenreSerializer(serializers.Serializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class TheatreHallSerializer(serializers.Serializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity"
        )



class PlaySerializer(serializers.Serializer):
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
    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "descriptions",
            "actors",
            "genres",
        )


class PlayDetailSerializer(PlayListSerializer):
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


class PerformanceSerializer(serializers.Serializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time",
        )


class PerformanceListSerializer(PerformanceSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "theatre_hall",
            "show_time",
        )


class ReservationSerializer(serializers.Serializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "created_at"
        )
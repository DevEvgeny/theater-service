from django.urls import path, include
from rest_framework import routers
from rest_framework.urls import app_name

from box_office.views import (
    ActorViewSet,
    GenreViewSet,
    TheatreHallViewSet,
    PerformanceViewSet, PlayViewSet, ReservationViewSet,
)

router = routers.DefaultRouter()

router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "box_office"
from django.urls import path, include
from rest_framework import routers
from rest_framework.urls import app_name

from box_office.views import (
    ActorViewSet
)

router = routers.DefaultRouter()

router.register("actors", ActorViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "box_office"
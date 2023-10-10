from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register(r"images", views.ImageViewSet)
links_router = routers.NestedSimpleRouter(router, r"images", lookup="image")
links_router.register(r"links", views.LinkViewSet, basename="image-links")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(links_router.urls)),
    path("<int:download_id>/", views.download, name="download"),
    path("<int:download_id>/<int:t>/", views.download, name="download_2"),
    path("link/<int:pk>/", views.download_link, name="download-link"),
]

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, authentication, permissions
from . import serializers
from .models import Image, Link
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django_sendfile import sendfile

# Create your views here.


class ImageViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Image.objects.all()
    serializer_class = serializers.ImageSerializer

    # def get_serializer_class(self):
    #     profile = self.request.user.profile

    #     return self.TIER_SERIALIZER["Enterprise"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return Image.objects.none()
        return qs.filter(user=request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def download(request, download_id, t=None):
    download = get_object_or_404(Image, pk=download_id)
    return _auth_download(request, download, t)


@login_required
def _auth_download(request, download, t=None):
    if not download.is_user_allowed(request.user):
        return HttpResponseForbidden("Sorry, you cannot access this file")
    path = download.image.path
    try:
        if t == 1:
            path = download.thumbnail_1.path
        elif t == 2:
            path = download.thumbnail_2.path
    except ValueError as e:
        return HttpResponseForbidden("Sorry, you cannot access this file")

    return sendfile(request, path)


class LinkViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]
    serializer_class = serializers.LinkSerializer

    def get_queryset(self):
        return Link.objects.filter(image=self.kwargs["image_pk"])

    def perform_create(self, serializer):
        serializer.save(image_id=self.kwargs["image_pk"])


def download_link(request, pk, t=None):
    try:
        link = Link.objects.get(pk=pk)
    except Link.DoesNotExist:
        return HttpResponseForbidden("Link has expired")
    return sendfile(request, link.image.image.path)

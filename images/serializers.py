from rest_framework import serializers
from .models import Image, Link
from rest_framework_nested.relations import NestedHyperlinkedRelatedField


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    thumbnail_1 = serializers.SerializerMethodField()
    thumbnail_2 = serializers.SerializerMethodField()
    original_image = serializers.SerializerMethodField()
    links = serializers.HyperlinkedIdentityField(
        view_name="image-links-list", lookup_url_kwarg="image_pk"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        profile = request.user.profile
        if not profile.height_1:
            self.fields.pop("thumbnail_1")
        if not profile.height_2:
            self.fields.pop("thumbnail_2")
        if not profile.original_link:
            self.fields.pop("original_image")
        if not profile.generate_link:
            self.fields.pop("links")

    class Meta:
        model = Image
        fields = (
            "url",
            "image",
            "original_image",
            "thumbnail_1",
            "thumbnail_2",
            "links",
        )
        extra_kwargs = {
            "image": {"write_only": True},
        }

    def get_thumbnail_1(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/{obj.id}/1/")

    def get_thumbnail_2(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/{obj.id}/2/")

    def get_original_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/{obj.id}/")


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ("valid", "link", "valid_till")
        extra_kwargs = {
            "valid": {"write_only": True},
        }

    def get_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/link/{obj.id}/")

from rest_framework import serializers
from core.models import Category, Site, SocialNetwork, SiteImages, Recommended


class CategorySerializer(serializers.ModelSerializer):
    """ Model serializer from Category model """
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'image')
        read_only_fields = ('id',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        instance = super().create(validated_data)
        instance.image.save(image.name, image)
        return instance

class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('id', 'site', 'link', 'type_social_network')
        read_only_fields = ('id',)

class SiteImagesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = SiteImages
        fields = ('id', 'site', 'image')
        read_only_fields = ('id',)

class SiteSerializer(serializers.ModelSerializer):
    """ Model serializer from site model """
    image = serializers.ImageField(required=False)
    social_networks = SocialNetworkSerializer(many=True, required=False)
    site_images = SiteImagesSerializer(many=True, required=False)


    class Meta:
        model = Site
        fields = ('id', 'name', 'url', 'location', 'quality', 'category', 'image', 'price', 'description', 'address', 'social_networks', 'site_images')
        read_only_fields = ('id',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        instance = super().create(validated_data)
        instance.image.save(image.name, image)
        return instance


class SiteListSerializer(SiteSerializer):
    class Meta(SiteSerializer.Meta):
        depth = 1


class RecommendedSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False)

    class Meta():
        model = Recommended
        fields = ('id', 'title', 'content', 'link', 'image',)


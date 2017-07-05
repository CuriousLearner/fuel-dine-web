from rest_framework import serializers

from .models import Restaurant, Comment, Review


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, required=True)
    lat = serializers.DecimalField(max_digits=15, decimal_places=10)
    lon = serializers.DecimalField(max_digits=15, decimal_places=10)
    description = serializers.CharField(max_length=500, required=False)
    address = serializers.CharField(max_length=500)

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantFormSerializer(RestaurantSerializer):

    class Meta:
        model = Restaurant
        fields = ('lat', 'lon', 'description', 'website', 'address', 'contact')


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=200)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentWithTextSerializer(CommentSerializer):

    class Meta:
        model = Comment
        fields = ('text', )


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewWithTextSerializer(ReviewSerializer):

    class Meta:
        model = Review
        fields = ('text', )


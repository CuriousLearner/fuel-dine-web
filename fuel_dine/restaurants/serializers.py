from rest_framework import serializers

from .models import Restaurant, Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=200)
    posted_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentReadOnlySerializer(CommentSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)
    posted_at = serializers.DateTimeField(required=False)
    comments = CommentReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewReadOnlySerializer(ReviewSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, required=True)
    lat = serializers.DecimalField(max_digits=25, decimal_places=15)
    lon = serializers.DecimalField(max_digits=25, decimal_places=15)
    description = serializers.CharField(max_length=500, required=False)
    address = serializers.CharField(max_length=500)
    is_active = serializers.BooleanField(default=True)
    reviews = ReviewReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantFormSerializer(RestaurantSerializer):

    class Meta:
        model = Restaurant
        fields = ('lat', 'lon', 'description', 'website', 'address', 'contact')

from rest_framework import serializers

from .models import Restaurant, Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=200)
    posted_at = serializers.DateTimeField(required=False)
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentPOSTSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=200)
    posted_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentWithTextSerializer(CommentSerializer):

    class Meta:
        model = Comment
        fields = ('text', )


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)
    posted_at = serializers.DateTimeField(required=False)
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = '__all__'


class ReviewPOSTSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)
    posted_at = serializers.DateTimeField(required=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class ReviewWithTextSerializer(ReviewSerializer):

    class Meta:
        model = Review
        fields = ('text', )


class RestaurantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, required=True)
    lat = serializers.DecimalField(max_digits=25, decimal_places=15)
    lon = serializers.DecimalField(max_digits=25, decimal_places=15)
    description = serializers.CharField(max_length=500, required=False)
    address = serializers.CharField(max_length=500)
    is_active = serializers.BooleanField(default=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantFormSerializer(RestaurantSerializer):

    class Meta:
        model = Restaurant
        fields = ('lat', 'lon', 'description', 'website', 'address', 'contact')

from django.forms import ModelForm, ValidationError

from .models import Restaurant, Review, Comment


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text']

    def clean(self):
        if self.cleaned_data['text'] != '':
            return super().clean()
        raise ValidationError('Review text cannot be blank')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def clean(self):
        if self.cleaned_data['text'] != '':
            return super().clean()
        raise ValidationError('Comment text cannot be blank')

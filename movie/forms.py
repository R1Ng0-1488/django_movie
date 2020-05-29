from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, RatingStar, Rating


class ReviewsForm(forms.ModelForm):
    """форма отзывов"""
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('email', 'name', 'message', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border'}),
            'message': forms.Textarea(attrs={'class': 'form-control border'}),
        }


class RatingForm(forms.ModelForm):
    """форма рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)

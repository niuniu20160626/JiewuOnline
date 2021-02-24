import re

from django import forms
from apps.operations.models import UserFavorite, CourseComments


class CommentsForm(forms.ModelForm):
    # model form
    class Meta:
        model = CourseComments
        fields = ["course","comments"]


class UserFavForm(forms.ModelForm):
    #model form
    class Meta:
        model = UserFavorite
        fields = ["fav_id","fav_type"]
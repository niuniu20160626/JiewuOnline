import re

from django import forms
from apps.operations.models import UserAsk, JchfComments


class JchfCommentsForm(forms.ModelForm):
    # model form
    class Meta:
        model = JchfComments
        fields = ["jchf","comments"]


class AddAskForm(forms.ModelForm):
    #model form
    mobile = forms.CharField(min_length=11, max_length=11, required=True)
    class Meta:
        model = UserAsk
        fields = ["name","mobile","course_name"]

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[3-9][0-9]{9}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
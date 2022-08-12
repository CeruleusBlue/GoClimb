from django import forms
from .models import MBPost

class MBPostForm(forms.ModelForm):
    class Meta:
        model = MBPost
        fields = '__all__'
    text = forms.Textarea
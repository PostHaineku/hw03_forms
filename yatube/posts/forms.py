from django import forms
from .models import New_post
from .models import Group

class New_post_form(forms.ModelForm):
    text = forms.CharField(widget= forms.Textarea)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False,
        label='Группа, к которой будет относиться пост',
        help_text='Выберите группу')
    class Meta:
        model = New_post
        fields = ('text', 'group')
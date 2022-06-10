from django import forms
from .models import Post
from .models import Group


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=False,
                                   label='Группа, к которой относится пост',
                                   help_text='Выберите группу')

    class Meta:
        model = Post
        fields = ('text', 'group')

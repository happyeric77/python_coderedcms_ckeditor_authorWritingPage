from django.forms import ModelForm
from .models import ArticlePage

class EditForm(ModelForm):
    class Meta:
        model = ArticlePage
        fields = ['draft', 'title']
from django.forms import ModelForm
from blog.models import Blog
from libs import CustomFormatter


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ('name', 'content', 'preview_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CustomFormatter.format_form_fields(self)


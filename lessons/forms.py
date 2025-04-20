
from django import forms
from .models import Lesson, LessonContent

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 1})
        }
class LessonContentForm(forms.ModelForm):
    class Meta:
            model = LessonContent
            fields = ['content_type', 'content', 'video_url', 'file', 'image', 'position']
            widgets = {
                'content_type': forms.Select(attrs={'class': 'form-select', 'id': 'content-type-select'}),
                'content': forms.Textarea(attrs={
                    'class': 'form-textarea',
                    'rows': 10,
                    'data-editor': 'true'
                }),
                'video_url': forms.URLInput(attrs={'class': 'form-input'}),
                'file': forms.FileInput(attrs={'class': 'form-file-input'}),
                'image': forms.FileInput(attrs={'class': 'form-file-input'}),
                'position': forms.NumberInput(attrs={'class': 'form-input', 'min': 0})
            }

    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('content_type')
        content = cleaned_data.get('content')
        video_url = cleaned_data.get('video_url')
        file = cleaned_data.get('file')
        image = cleaned_data.get('image')

        if content_type == 'video' and not video_url:
            self.add_error('video_url', 'Для видео необходимо указать ссылку.')
        elif content_type == 'file' and not file:
            self.add_error('file', 'Необходимо загрузить файл.')
        elif content_type == 'image' and not image:
            self.add_error('image', 'Необходимо загрузить изображение.')
        elif content_type in ['text', 'code', 'markdown'] and not content:
            self.add_error('content', 'Необходимо заполнить содержимое.')

        return cleaned_data
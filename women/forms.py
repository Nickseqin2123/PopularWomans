from django import forms
from .models import Category, Husband, Women
from captcha.fields import CaptchaField

    
class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label='Не замужем', required=False, label='Муж')

    class Meta:
        model = Women
        fields = ('title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {
            'slug': 'URL'
        }
        

class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.CharField(label='E-mail')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
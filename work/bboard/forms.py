from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput


class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=20)  # ограничение на длину описания

    class Meta:
        model = Post
        fields = ('title', 'content', 'author', 'type', 'price', 'image')

        def clean(self):
            cleaned_data = super().clean()  # вызываем метод родителя
            content = cleaned_data.get("content")   # получаем значение для поля content
            # if content is not None and len(content) < 10:    # если описание меньше 10 символов, то ошибка!
            #     raise ValidationError({    # ошибка валидации
            #         "content": "Описание не может быть меньше, чем 10 символов!"})

            title = cleaned_data.get("title")    # получаем значение для поля title
            if title == content:  # если название и описание равны, то ошибка!
                raise ValidationError({       # ошибка валидации
                    "title": "Название не должно быть идентичным описанию"})
            return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'author')
        # widgets = {
        #     'content': forms.Textarea(attrs={'rows': 2, 'cols': 50})
        # }
        # labels = {
        #     'content': 'Комментарий',
        #     'author': 'Автор'
        # }
        # help_texts = {
        #     'content': 'Напишите комментарий',
        #     'author': 'Введите имя'
        # }
        # error_messages = {
        #     'content': {
        #         'required': 'Комментарий не может быть пустым',
        #         'max_length': 'Комментарий не может быть длиннее 250 символов'
        #     },
        # }

        def clean_content(self):
            content = self.cleaned_data.get('content')
            if len(content) < 10:
                raise ValidationError('Комментарий не может быть меньше, чем 10 символов')
            return content

        def clean_author(self):
            author = self.cleaned_data.get('author')
            if len(author) < 3:
                raise ValidationError('Имя не может быть меньше, чем 3 символа')
            return author


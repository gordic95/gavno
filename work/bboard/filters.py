from django_filters import FilterSet
from .models import *
from django_filters import ModelChoiceFilter
# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
    post = ModelChoiceFilter(
        empty_label='Все обьявления',
        field_name='post',
        label='фильтр по обьявлениям',
        queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('post',)

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author=self.request.user)


    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': ['icontains'],
    #         'type': ['exact']
    #     }

# В Meta классе мы должны указать Django модель,# в которой будем фильтровать записи.
# В fields мы описываем по каким полям модели # будет производиться фильтрация.
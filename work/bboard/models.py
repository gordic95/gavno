from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.conf import settings


# def user_directory_path(instance, filename):
#     return 'user_{0}/{1}'.format(instance.user.id, filename)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'
        ordering = ['user__username']


class Post(models.Model):
    TYPES = [
        ('TANK', 'Танк'),
        ('HILL', 'Хил'),
        ('DD', 'ДД'),
        ('VEND', 'Торговец'),
        ('GM', 'Гилдмастер'),
        ('KVG', 'Квестгивер'),
        ('BS', 'Кузнец'),
        ('TANER', 'Кожевник'),
        ('ALCH', 'Зельевар'),
        ('MAG', 'Мастер заклинаний'),
    ]
    title = models.CharField(max_length=200, verbose_name='Название товар')
    content = models.TextField(verbose_name='Описание товара')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    type = models.CharField(max_length=5, choices=TYPES, blank=False, verbose_name='Категория')
    price = models.FloatField(validators=[MinValueValidator(0.0)], verbose_name='Цена')
    image = models.ImageField(upload_to='image/', verbose_name='Изображение', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    #Мы используем специальную функцию reverse, которая позволяет нам указывать не путь вида /products/…, а название пути.
    #Чтобы после создание новости возвращало к этой новости

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Обьявление')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Описание')
    status = models.BooleanField(default=False, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.author} : {self.content}[:20] + ...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])

    # def accepted(self):
    #     self.status = True
    #     self.save()

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['id']



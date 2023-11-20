from .models import Post, Author
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import PostFilter
from .forms import PostForm, CommentForm

from django.urls import reverse_lazy
from .models import Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 8

    # Добавляем параметр для фильтрации
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    paginate_by = 8

    # def get_object(self, **kwargs):
    #     obj = cache.get(f'post: {self.kwargs["pk"]}', None)
    #
    #     if not obj:
    #         obj = super().get_object(queryset=self.queryset)
    #         cache.set(f'post: {self.kwargs["pk"]}', obj)
    #     return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["pk"])
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
# Обратите внимание, в представлении мы также не указываем форму. Вместо неё появляется поле success_url, в которое мы должны указать, куда перенаправить пользователя после успешного удаления товара. Логика работы reverse_lazy точно такая же, как и у функции reverse, которую мы использовали в моделе Product.


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'create_comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    # если не прошел авторизацию, то добавить комментарий не сможешь


class PostsUserComments(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'posts_user_comments.html'
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        queryset = Comment.objects.filter(post__author__id=self.request.user.pk).order_by('-create_at')
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset, request=self.request.user.pk)
        return context


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        queryset = Comment.objects.filter(post__author__id=self.request.user.pk).order_by('create_at')
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset, request=self.request.user.pk)
        return context











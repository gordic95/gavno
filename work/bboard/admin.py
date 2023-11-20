from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'content', 'created_at', 'author')
    list_filter = ('title', 'content', 'type')
    search_fields = ('title', 'content')

    # def make_published(self, request, queryset):
    #     queryset.update(status='p')
    #     self.message_user(request, 'Posts marked as published')
    #     return None
    # make_published.short_description = 'Mark selected posts as published'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content')
    list_filter = ('post', 'author', 'content')
    search_fields = ('post', 'author', 'content')
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content')
        }),

    )


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)




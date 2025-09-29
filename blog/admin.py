from django.contrib import admin
from .models import Post, Profile, Comment, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'published')
    list_filter = ('published', 'created', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created'
    ordering = ('-created',)

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author', 'published')
        }),
        ('Timestamps', {
            'fields': ('created', ),
            'classes': ('collapse',),
        }),
        
    )

admin.site.site_header = "Blog Administration"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Welcome to the Blog Admin Area"
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Profile)
admin.site.register(Post, PostAdmin)


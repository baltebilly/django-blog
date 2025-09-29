from django.contrib import admin
from .models import Post, Profile


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

    
admin.site.register(Profile)
admin.site.register(Post, PostAdmin)


"""
Blog Admin Configuration
=============================================
This module configures the Django admin interface for the blog application.
It registers models and customizes their presentation and functionality in the admin site.
"""

from django.contrib import admin
from .models import Category, Post, Comment

class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    
    Features:
    - List display shows name and slug
    - Auto-populates slug from name
    - Search by name
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class CommentInline(admin.TabularInline):
    """
    Inline admin configuration for comments.
    
    Shows comments directly on the post edit page in a tabular format.
    Comments are readonly in this view, but can be deleted.
    """
    model = Comment
    extra = 0  # No empty forms
    readonly_fields = ('name', 'email', 'content', 'created_on')
    can_delete = True
    max_num = 0  # No limit on the number of comments shown

class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    
    Features:
    - Customized list display with post details
    - Filtering options by status, category, and date
    - Search by title and content
    - Auto-populated slug from title
    - Custom action to publish posts
    - Inline display of comments
    """
    list_display = ('title', 'author', 'status', 'created_on')
    list_filter = ('status', 'categories', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_published']
    inlines = [CommentInline]
    readonly_fields = ('created_on', 'updated_on')
    
    def make_published(self, request, queryset):
        """
        Custom admin action to mark selected posts as published.
        
        Changes the status of selected posts to '1' (Published).
        
        Args:
            request: The current request
            queryset: The selected posts
        """
        queryset.update(status=1)
    make_published.short_description = "Mark selected posts as published"

class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    
    Features:
    - List display with comment details
    - Filtering by approval status and date
    - Search by commenter name, email, and content
    - Custom action to approve comments
    """
    list_display = ('name', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        """
        Custom admin action to approve selected comments.
        
        Changes the 'approved' status of selected comments to True.
        
        Args:
            request: The current request
            queryset: The selected comments
        """
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"

# Register models with the admin site using their custom admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

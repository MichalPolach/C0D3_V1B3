"""
Blog Models - Data structure for the blog application
=============================================
This module defines the database models for the blog application.
It includes models for Categories, Posts, and Comments,
with appropriate relationships between them.
"""

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField

class Category(models.Model):
    """
    Category model for classifying blog posts.
    
    Each category has a name and slug for URL-friendly representation.
    Posts can belong to multiple categories.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        """
        String representation of a category.
        
        Returns:
            str: The category name
        """
        return self.name
    
    def get_absolute_url(self):
        """
        Returns the URL for viewing this category's posts.
        
        Returns:
            str: URL to the category detail page
        """
        return reverse('blog:category', args=[self.slug])

class Post(models.Model):
    """
    Post model representing a blog article.
    
    Contains all details of a blog post including title, content,
    author, publication status, and relationships to categories.
    Uses Django MDEditor for rich Markdown content.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='blog_posts'
    )
    content = MDTextField()  # Markdown editor field
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(
        Category, 
        related_name='posts'
    )
    status = models.IntegerField(
        choices=[(0, "Draft"), (1, "Published")], 
        default=0
    )
    
    class Meta:
        ordering = ['-created_on']  # Newest posts first
    
    def __str__(self):
        """
        String representation of a post.
        
        Returns:
            str: The post title
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Returns the URL for viewing this post.
        
        Returns:
            str: URL to the post detail page
        """
        return reverse('blog:post_detail', args=[self.slug])

class Comment(models.Model):
    """
    Comment model for user-submitted comments on blog posts.
    
    Links to a specific post and includes commenter information.
    Comments require approval by admin before being displayed.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Requires admin approval
    
    class Meta:
        ordering = ['created_on']  # Oldest comments first
    
    def __str__(self):
        """
        String representation of a comment.
        
        Returns:
            str: Description including commenter name and post title
        """
        return f'Comment by {self.name} on {self.post}'

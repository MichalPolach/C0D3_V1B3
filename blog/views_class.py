"""
Blog Views - Handles all view logic for the blog application
=============================================
This module contains all view classes and functions that power the blog application.
It includes list views for displaying posts, detail views for individual posts,
category filtering, date-based archives, and the about page.

The architecture follows Django's class-based views pattern with a custom mixin
for shared functionality across views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from .models import Post, Category, Comment
import datetime

class BlogContextMixin:
    """
    Mixin that provides common context data for all blog views.
    
    This mixin centralizes the logic for fetching categories and archives
    that are displayed in the sidebar across all pages of the blog.
    By using this mixin, we avoid code duplication in view classes.
    """
    def get_common_context(self):
        """
        Returns a dictionary with categories and archives for the sidebar.
        
        Returns:
            dict: Context containing categories and archives
        """
        context = {}
        context['categories'] = Category.objects.all()
        context['archives'] = self.get_archives()
        return context
    
    def get_archives(self):
        """
        Organizes published posts by year and month for the archive sidebar.
        
        Fetches all dates with published posts and organizes them in a nested
        dictionary structure with years as keys and lists of date objects as values.
        
        Returns:
            dict: Dictionary with years as keys and lists of datetime objects as values
        """
        # Get years and months with posts
        dates = Post.objects.filter(status=1).dates('created_on', 'month', order='DESC')
        archives = {}
        for date in dates:
            year = date.year
            if year not in archives:
                archives[year] = []
            if date not in archives[year]:
                archives[year].append(date)
        return archives

class PostList(BlogContextMixin, generic.ListView):
    """
    View for the blog homepage displaying a paginated list of published posts.
    
    Inherits from BlogContextMixin to include sidebar data and
    Django's ListView for pagination and template rendering.
    """
    queryset = Post.objects.filter(status=1).order_by('-created_on')  # Only published posts, newest first
    template_name = 'blog/home.html'
    paginate_by = 5  # Show 5 posts per page
    context_object_name = 'posts'  # Template variable name for the post list
    
    def get_context_data(self, **kwargs):
        """
        Adds common sidebar context to the view's context.
        
        Args:
            **kwargs: Default context from parent class
            
        Returns:
            dict: Context with posts and sidebar data
        """
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        return context

class PostDetail(BlogContextMixin, generic.DetailView):
    """
    View for displaying a single blog post and handling comment submissions.
    
    Displays a post with its details, comments, and a comment form.
    Also handles the POST requests for comment submissions.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """
        Ensures only published posts are accessible.
        
        Returns:
            QuerySet: Filtered queryset with only published posts
        """
        return Post.objects.filter(status=1)
    
    def get_context_data(self, **kwargs):
        """
        Adds comments and sidebar data to the context.
        
        Args:
            **kwargs: Default context from parent class
            
        Returns:
            dict: Context with post, comments, and sidebar data
        """
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(approved=True).order_by('created_on')
        context.update(self.get_common_context())
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handles comment submission for the current post.
        
        Validates the comment form data and creates a new comment if valid.
        Shows success or error messages to the user.
        
        Args:
            request: HTTP request
            *args, **kwargs: Arguments passed to the view
            
        Returns:
            HttpResponse: Redirect to the post detail page
        """
        post = self.get_object()
        
        # Handle comment submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        if name and email and content:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                content=content
            )
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
        else:
            messages.error(request, 'Please fill in all the required fields.')
        
        return redirect(post.get_absolute_url())

class CategoryView(BlogContextMixin, generic.ListView):
    """
    View for displaying posts filtered by category.
    
    Shows a list of posts belonging to a specific category.
    """
    template_name = 'blog/category.html'
    paginate_by = 5
    context_object_name = 'posts'
    
    def get_queryset(self):
        """
        Filters posts by the requested category slug.
        
        Retrieves the Category object specified in the URL slug
        and returns all published posts in that category.
        
        Returns:
            QuerySet: Published posts in the specified category
        """
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(categories=self.category, status=1).order_by('-created_on')
    
    def get_context_data(self, **kwargs):
        """
        Adds category info and sidebar data to the context.
        
        Args:
            **kwargs: Default context from parent class
            
        Returns:
            dict: Context with posts, category info, and sidebar data
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context.update(self.get_common_context())
        return context

class ArchiveView(BlogContextMixin, generic.ListView):
    """
    View for displaying posts filtered by year or month.
    
    Handles both year-based and month-based archive views using the same class.
    """
    template_name = 'blog/archive.html'
    paginate_by = 5
    context_object_name = 'posts'
    
    def get_queryset(self):
        """
        Filters posts by year and optional month.
        
        Depending on the URL parameters, returns posts from a specific year
        or from a specific month within a year.
        
        Returns:
            QuerySet: Published posts filtered by date
        """
        year = self.kwargs['year']
        month = self.kwargs.get('month', None)
        
        if month:
            # Month archive view
            self.date = datetime.date(year=int(year), month=int(month), day=1)
            return Post.objects.filter(
                created_on__year=year,
                created_on__month=month,
                status=1
            ).order_by('-created_on')
        else:
            # Year archive view
            self.date = datetime.date(year=int(year), month=1, day=1)
            return Post.objects.filter(
                created_on__year=year,
                status=1
            ).order_by('-created_on')
    
    def get_context_data(self, **kwargs):
        """
        Adds archive title and sidebar data to the context.
        
        Creates a user-friendly title for the archive page (e.g., "June 2023")
        and adds it to the context along with sidebar data.
        
        Args:
            **kwargs: Default context from parent class
            
        Returns:
            dict: Context with posts, archive title, and sidebar data
        """
        context = super().get_context_data(**kwargs)
        context.update(self.get_common_context())
        
        if 'month' in self.kwargs:
            # Format like "June 2023"
            context['archive_title'] = self.date.strftime("%B %Y")
        else:
            # Just the year
            context['archive_title'] = self.kwargs['year']
            
        return context

def about(request):
    """
    View function for the about page.
    
    A simple function-based view that renders the about page template
    with the common sidebar context data.
    
    Args:
        request: HTTP request
        
    Returns:
        HttpResponse: Rendered about page
    """
    # Create a mixin instance to access its methods
    mixin = BlogContextMixin()
    context = mixin.get_common_context()
    return render(request, 'blog/about.html', context)
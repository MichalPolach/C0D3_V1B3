"""
Blog Views - Handles all view logic for the blog application
=============================================
This module contains all view functions that power the blog application.
It includes views for displaying post lists, post details, category filtering,
date-based archives, and the about page.

The architecture follows Django's function-based views pattern with helper
functions for shared functionality across views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Comment
import datetime

def get_archives():
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

def get_common_context():
    """
    Returns a dictionary with categories and archives for the sidebar.
    
    Returns:
        dict: Context containing categories and archives
    """
    context = {}
    context['categories'] = Category.objects.all()
    context['archives'] = get_archives()
    return context

def post_list(request):
    """
    View for the blog homepage displaying a paginated list of published posts.
    
    Args:
        request: HTTP request
        
    Returns:
        HttpResponse: Rendered homepage with paginated posts and sidebar
    """
    # Get published posts, newest first
    post_list = Post.objects.filter(status=1).order_by('-created_on')
    
    # Set up pagination
    paginator = Paginator(post_list, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    # Build context with posts and sidebar data
    context = {
        'posts': posts,
    }
    context.update(get_common_context())
    
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    """
    View for displaying a single blog post and handling comment submissions.
    
    Displays a post with its details, comments, and a comment form.
    Also handles the POST requests for comment submissions.
    
    Args:
        request: HTTP request
        slug: Post slug from URL
        
    Returns:
        HttpResponse: Rendered post detail page or redirect after comment
    """
    # Get the post, ensuring it's published
    post = get_object_or_404(Post.objects.filter(status=1), slug=slug)
    
    # Handle comment submission if POST request
    if request.method == 'POST':
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
    
    # For GET requests, prepare and render the template
    comments = post.comments.filter(approved=True).order_by('created_on')
    
    context = {
        'post': post,
        'comments': comments,
    }
    context.update(get_common_context())
    
    return render(request, 'blog/post_detail.html', context)

def category_view(request, slug):
    """
    View for displaying posts filtered by category.
    
    Shows a list of posts belonging to a specific category.
    
    Args:
        request: HTTP request
        slug: Category slug from URL
        
    Returns:
        HttpResponse: Rendered category page with filtered posts
    """
    # Get the category
    category = get_object_or_404(Category, slug=slug)
    
    # Get published posts in this category
    post_list = Post.objects.filter(categories=category, status=1).order_by('-created_on')
    
    # Set up pagination
    paginator = Paginator(post_list, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    # Build context with posts, category and sidebar data
    context = {
        'posts': posts,
        'category': category,
    }
    context.update(get_common_context())
    
    return render(request, 'blog/category.html', context)

def archive_view(request, year, month=None):
    """
    View for displaying posts filtered by year or month.
    
    Handles both year-based and month-based archive views.
    
    Args:
        request: HTTP request
        year: Year to filter by
        month: Optional month to filter by
        
    Returns:
        HttpResponse: Rendered archive page with filtered posts
    """
    # Convert string params to integers
    year = int(year)
    
    # Filter posts by date
    if month:
        month = int(month)
        date = datetime.date(year=year, month=month, day=1)
        post_list = Post.objects.filter(
            created_on__year=year,
            created_on__month=month,
            status=1
        ).order_by('-created_on')
        archive_title = date.strftime("%B %Y")  # Format like "June 2023"
    else:
        date = datetime.date(year=year, month=1, day=1)
        post_list = Post.objects.filter(
            created_on__year=year,
            status=1
        ).order_by('-created_on')
        archive_title = str(year)  # Just the year
    
    # Set up pagination
    paginator = Paginator(post_list, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    # Build context with posts, archive title and sidebar data
    context = {
        'posts': posts,
        'archive_title': archive_title,
    }
    context.update(get_common_context())
    
    return render(request, 'blog/archive.html', context)

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
    context = get_common_context()
    return render(request, 'blog/about.html', context)

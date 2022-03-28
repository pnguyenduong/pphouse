from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Post, Author, Category


def search(request):
    categories = Category.objects.all()
    post_queryset = Post.objects.all()
    recent_posts = Post.objects.order_by('-timestamp')[0:3]
    query = request.GET.get('q')
    if query:
        search_post_queryset = post_queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(content__icontains=query) |
            Q(categories__title__icontains=query)
        ).distinct()
        context = {
            'post_list': search_post_queryset,
            'categories': categories,
            'recent_posts': recent_posts
        }

    return render(request, 'blog/pages/search_page.html', context)

def get_author(user):
    queryset = Author.objects.filter(user=user)
    if queryset.exists():
        return queryset[0]
    return None




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Author, PostView, Category
from .forms import CommentForm, PostForm
from .tools import get_author
from marketing.forms import EmailSignupForm


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        recent_posts = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'featured': featured,
            'recent_posts': recent_posts,
            'form': self.form
        }
        return render(request, 'blog/pages/index.html', context)

class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog/pages/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 4
    ordering = ['-timestamp']

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        recent_posts = Post.objects.order_by('-timestamp')[0:3]
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['recent_posts'] = recent_posts
        context['form'] = self.form
        return context

class CategoryListView(ListView):
    model = Post
    template_name = 'blog/pages/category_list.html'
    context_object_name = 'post_list'
    
    def get_context_data(self, **kwargs):
        slug = get_object_or_404(Category, slug=self.kwargs['slug'])
        category = Category.objects.filter(slug__icontains=slug)
        queryset = Post.objects.filter(categories=category[0])
        recent_posts = Post.objects.order_by('-timestamp')[0:3]
        categories = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['recent_posts'] = recent_posts
        context['post_list'] = queryset
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post_detail.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        most_recent = Post.objects.order_by('-timestamp')[:3]
        categories = Category.objects.all()
        recent_posts = Post.objects.order_by('-timestamp')[0:3]
        context = super().get_context_data(**kwargs)
        context['categories'] = categories
        context['recent_posts'] = recent_posts
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'slug': post.slug
            }))

class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/pages/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        messages.add_message(self.request, messages.INFO, 'Your post has been created..!')
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/pages/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        messages.add_message(self.request, messages.INFO, 'Your post has been updated..!')
        return redirect(reverse("post-detail", kwargs={
            'slug': form.instance.slug
        }))


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'blog/pages/post_confirm_delete.html'
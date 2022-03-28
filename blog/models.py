from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify

from tinymce import HTMLField

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(max_length=300)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        ordering = ['title',]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

        super(Category, self).save(*args, **kwargs)

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail_url = models.URLField(max_length=300)
    slug = models.SlugField(null=False, unique=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    content = HTMLField('Content')
    previous_post = models.ForeignKey('self', related_name='pervious', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
    def get_update_url(self):
        return reverse('post-update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'slug': self.slug})

    @property
    def get_comments(self):
        return self.comments.order_by('-timestamp').all()
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()
    
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


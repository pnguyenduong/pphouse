from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostView)


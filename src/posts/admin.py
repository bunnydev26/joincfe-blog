from django.contrib import admin
from .models import Post

# Register your models here.
#@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'content', 'created', 'last_updated']
	list_display_links = ['content']
	list_filter = ['last_updated', 'created']
	search_fields = ['title']

admin.site.register(Post, PostAdmin)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
# Create your views here.

def post_create(request):
	return HttpResponse("Hello this is posts Create")

def post_detail(request, id=None):
	context = {}
	post_instance = get_object_or_404(Post, id=id)
	context['post_instance'] = post_instance
	return render(request, 'post_detail.html', context=context)

def post_list(request):
	context = {}
	context['post_list'] = Post.objects.all()
	return render(request, 'index.html', context=context)

def post_update(request):
	return HttpResponse("Hello this is posts update")

def post_delete(request):
	return HttpResponse("Hello this is posts delete")


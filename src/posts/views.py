from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
# Create your views here.
from .forms import PostForm

def post_create(request):
	context = {}
	if request.method == 'POST':
		post_form = PostForm(data=request.POST or None)
		context["post_form"] = post_form

		if post_form.is_valid():
			instance = post_form.save(commit=False)
			instance.save()
			# Message
			messages.success(request, "successfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())
		else:
			messages.error(request, "Could not save")
	else:
		post_form = PostForm()
		context["post_form"] = post_form

	context["btn_text"] = "Create"
	return render(request, "post_form.html", context=context)

def post_detail(request, id=None):
	context = {}
	post_instance = get_object_or_404(Post, id=id)
	context['title'] = 'Detail'
	context['post_instance'] = post_instance
	return render(request, 'post_detail.html', context=context)

def post_list(request):
	context = {}
	context['post_list'] = Post.objects.all()
	context['title'] = "List"
	return render(request, 'post_list.html', context=context)

def post_update(request, id=None):
	context = {}
	post_instance = get_object_or_404(Post, id=id)
	post_form = None

	if request.method == 'POST':
		post_form = PostForm(data=request.POST or None, instance=post_instance)
		if post_form.is_valid():
			instance = post_form.save(commit=False)
			instance.save()
			# Message
			messages.success(request, "successfully updated", extra_tags="html_safe")
			return HttpResponseRedirect(instance.get_absolute_url())

		else:
			messages.error(request, "Could not update")
	else:
		post_form = PostForm(instance=post_instance)

	context["post_form"] = post_form
	context["btn_text"] = "Update"

	return render(request, "post_form.html", context=context)

def post_delete(request, id=None):
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "successfully Deleted")
	return redirect("posts:list")


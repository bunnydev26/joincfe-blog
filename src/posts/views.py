from urllib import quote_plus
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
# Create your views here.
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	context = {}
	if request.method == 'POST':
		post_form = PostForm(data=request.POST or None, files=request.FILES or None)
		context["post_form"] = post_form

		if post_form.is_valid():
			instance = post_form.save(commit=False)
			instance.user = request.user
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

def post_detail(request, slug=None):
	context = {}
	post_instance = get_object_or_404(Post, slug=slug)

	if post_instance.draft or post_instance.publish > timezone.now().date():
		if (not request.user.is_staff or not request.user.is_superuser):
			raise Http404

	context['title'] = 'Detail'
	context['post_instance'] = post_instance
	context['share_string'] = quote_plus(post_instance.content)
	return render(request, 'post_detail.html', context=context)

def post_list(request):
	context = {}
	if request.user.is_staff or request.user.is_superuser:
		post_list = Post.objects.all()
	else:
		post_list = Post.objects.active()

	query = request.GET.get("q")
	if query:
		post_list = post_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()

	today = timezone.now().date()
	paginator = Paginator(post_list, 2) # Show 25 contacts per page
	page_request = 'page'

	page = request.GET.get(page_request)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		posts = paginator.page(paginator.num_pages)

	context['title'] = "List"
	context['posts'] = posts
	context['page_request'] = page_request
	context['today'] = today
	return render(request, 'post_list.html', context=context)

def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	context = {}
	post_instance = get_object_or_404(Post, slug=slug)
	post_form = None

	if request.method == 'POST':
		post_form = PostForm(data=request.POST or None, instance=post_instance, files=request.FILES or None)
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

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "successfully Deleted")
	return redirect("posts:list")


from .forms import CommentForm, CvForm, PostForm
from .models import Comment, Cv, Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})
	
@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)
	
def cv(request, pk):
	cv = get_object_or_404(Cv, pk=pk)
	return render(request, 'cv/cv.html', {'cv': cv})
	
@login_required
def cv_edit(request, pk):
	cv = get_object_or_404(Cv, pk=pk)
	if request.method == 'POST':
		form = CvForm(request.POST, instance=cv)
		if form.is_valid():
			cv = form.save(commit=False)
			cv.save()
			return redirect('cv', pk=cv.pk)
	else:
		form = CvForm(instance=cv)
	return render(request, 'cv/cv_edit.html', {'form': form})
	
@login_required
def cv_new(request):
	if request.method == 'POST':
		form = CvForm(request.POST)
		if form.is_valid():
			cv = form.save(commit=False)
			cv.save()
			return redirect('cv', pk=cv.pk)
	else:
		form = CvForm()
	return render(request, 'cv/cv_new.html', {'form': form})
	
def cv_none(request):
	return render(request, 'cv/cv_none.html')
	
@login_required
def cv_remove(request, pk):
	cv = get_object_or_404(Cv, pk=pk)
	cv.delete()
	return redirect('cvs')
	
def cvs(request):
	cvs = Cv.objects.all()
	if not cvs:
		return redirect('cv_none')
	else:
		cv = cvs.last()
		return redirect('cv', pk=cv.pk)
		
@login_required
def cvs_edit(request):
	cvs = Cv.objects.all()
	if not cvs:
		return redirect('cv_none')
	else:
		cv = cvs.last()
		return redirect('cv_edit', pk=cv.pk)
		
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
	
@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})
	
@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})
	
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
	
@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_new.html', {'form': form})
	
@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)
	
@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')

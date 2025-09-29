from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import localtime

from .models import Post, Comment, Like
from .forms import PostForm, ProfileForm, CommentForm


# ==========================
# 🔹 POSTS
# ==========================

def post_list(request):
    posts_qs = Post.objects.filter(published=True).order_by("-created")
    paginator = Paginator(posts_qs, 3)  # 3 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by("-created")

    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()

    # Handle normal comment form (non-AJAX fallback)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect("post_detail", pk=pk)
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
        "is_liked": is_liked,
        "total_likes": post.likes.count(),
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # ✅ request.FILES added
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect(post.get_absolute_url())
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  # ✅ request.FILES added
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form, "post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return render(request, "blog/post_confirm_delete.html", {"post": post})


# ==========================
# 🔹 LIKES
# ==========================

@login_required
@require_POST
def ajax_toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:  # already liked → unlike
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": post.likes.count(),
    })


# ==========================
# 🔹 COMMENTS
# ==========================

@login_required
@require_POST
def ajax_add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get("content", "").strip()
    if content:
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=content
        )
        return JsonResponse({
            "id": comment.id,
            "username": comment.user.username,
            "created": localtime(comment.created).strftime("%b %d, %Y %H:%M"),
            "content": comment.content,
        })
    return JsonResponse({"error": "No content"}, status=400)


@login_required
@require_POST
def ajax_delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk, user=request.user)
        comment.delete()
        return JsonResponse({"deleted": True})
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Not allowed."}, status=403)


# ==========================
# 🔹 PROFILE
# ==========================

@login_required
def profile_detail(request):
    profile = request.user.profile
    return render(request, "blog/profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "blog/edit_profile.html", {"form": form})


# ==========================
# 🔹 AUTH / REGISTER
# ==========================

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile_detail")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

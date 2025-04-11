from .models import Post, Comment
from .forms import PostForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone


# def home(request):
#     # Eng yangi postlar
#     latest_posts = Post.objects.filter(is_approved=True).order_by('-created_at')[:5]

#     # Eng ko'p ko‘rilgan postlar
#     most_viewed_posts = Post.objects.filter(is_approved=True).order_by('-views')[:5]

#     # Haftaning eng ommabop postlari
#     one_week_ago = timezone.now() - timedelta(days=7)
#     weekly_popular_posts = Post.objects.filter(is_approved=True, created_at__gte=one_week_ago).order_by('-views')[:5]

#     # Oyning eng ommabop postlari
#     one_month_ago = timezone.now() - timedelta(days=30)
#     monthly_popular_posts = Post.objects.filter(is_approved=True, created_at__gte=one_month_ago).order_by('-views')[:5]

#     # Tavsiya qilingan postlar
#     recommended_posts = Post.objects.filter(is_approved=True, is_recommended=True)[:5]

#     return render(request, 'blog/home.html', {
#         'latest_posts': latest_posts,
#         'most_viewed_posts': most_viewed_posts,
#         'weekly_popular_posts': weekly_popular_posts,
#         'monthly_popular_posts': monthly_popular_posts,
#         'recommended_posts': recommended_posts,
#     })


# Post detail view
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    # Ko'rilganlar sonini oshirish
    post.views += 1
    post.save()

    # Foydalanuvchi izoh qoldirsa
    if request.method == 'POST':
        comment_author = request.POST.get('author')
        comment_text = request.POST.get('text')
        Comment.objects.create(post=post, author=comment_author, text=comment_text)
        return redirect('post_detail', pk=post.pk)

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


# Register view
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             login(request, form.save())
#             return redirect('home')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'blog/register.html', {'form': form})


# @login_required
# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user  # Foydalanuvchi nomi bilan postni bog'lash
#             post.save()
#             return redirect('home')  # Yangi post qo'shilgandan so'ng home sahifasiga o'tish
#     else:
#         form = PostForm()
#     return render(request, 'blog/create_post.html', {'form': form})


# def custom_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_approved = False  # Tasdiqlanmagan post
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return redirect('home')
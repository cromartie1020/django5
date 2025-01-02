from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
def post_list(request):
    post_list = Post.published.all()
    # Pagingator with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)
    posts=paginator.page(page_number)
    context={
        'posts':posts
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(
        request,
        'blog/post_detail.html',
        {'post': post}
    )
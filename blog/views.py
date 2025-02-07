from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect 
from django.http import Http404
from .models import Post
from .forms import EmailPostForm, CommentForm, Comment
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from taggit.models import Tag
from . forms import PostForm


def post_list(request):
    post_list = Post.published.all()
    # Pagingator with 3 posts per page
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)    
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    
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

def post_share(request, post_id):
    # Retrieve post by id. 
    post=get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    sent=False
    if request.method == 'POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url=request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (f"{cd['name']} ({cd['email']}) " 
                      f"recommends you read {post.title}"
            )        
            message = (
                f"Read {'post.title'} at {post_url}\n\n" 
                f"{cd['name']}\'s comments:{cd['comments']}"
            )    
                
            send_mail(subject=subject,
                      message=message,
                      from_email='cromarties2913@gmailcom',
                      recipient_list=[cd['to']]
            )
            sent = True    
    else:
        form = EmailPostForm()
            
    context={
        'post':post,
        'form':form,
        'sent':sent
    }    
    return render(request,'blog/share.html', context) 
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'blog/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        },
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                )
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )

    return render(
        request,
        'blog/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        },
    )

def post_update(request, id):
    pass

def post_new(request):
    if request.method ==('POST' or None):
        form = PostForm(request.POST) 
        
        if form.is_valid():
            form.save()
            
            return redirect('post_list')
    else:
        form=PostForm()
   
    context = {
        'form':form
    }         
    
    return render(request, 'blog/post_new.html', context)
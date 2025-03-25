from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Post
from django.core.paginator import Paginator

# # posts = [
#         {
#             'id': 1,
#             'title': 'First Post',
#             'content': 'This is the first post'
#             },
#         {
#             'id': 2,
#             'title': 'Second Post',
#             'content': 'This is the second post'
#         },
#         {
#             'id': 3,
#             'title': 'Third Post',
#             'content': 'This is the third post'
#         },
#         {
#             'id': 4,
#             'title': 'Fourth Post',
#             'content': 'This is the fourth post'
#         },
#         {
#             'id': 5,
#             'title': 'Fifth Post',
#             'content': 'This is the fifth post'
#         },
#         {
#             'id': 6,
#             'title': 'Sixth Post',
#             'content': 'This is the sixth post'
#         }
# ]


def index(request):
    posttitle = "Lastest Post"
    pagetitle = "Blog"
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'posttitle': posttitle, 'pagetitle': pagetitle, 'pages': pages})


def details(request, slug):
    #post = next((item for item in Post.objects.all() if item['id'] == int(post_id)), None)
   # logger = logging.getLogger("Test")
   # logger.debug(f"Test debug {post}")
    try:
        post = Post.objects.get(slug=slug)  
        related_post = Post.objects.filter(category=post.category).exclude(slug=post.slug)                                                     
    except Post.DoesNotExist:
        raise Http404
    return render(request, 'blog/details.html', {'post': post, 'related_post': related_post})   


def old_url(request):
    return redirect(reverse('blog:new_url_reverse'))


def new_url(request):
    return HttpResponse("Hello, world. You're at the new url.")
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
import logging
from .models import Post, About_us, Category
from django.core.paginator import Paginator
from .forms import ContactForm, RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, PostForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
    paginator = Paginator(posts, 6)
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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        logger = logging.getLogger("Test")
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if form.is_valid():
            logger.debug(f"Test debug {form.cleaned_data['name'] } {form.cleaned_data['email']} {form.cleaned_data['message']}")
            #send email
            success_message = "your mail has been sent"
            return render(request, 'blog/contact.html', {'form': form , 'name': name, 'email': email, 'message': message, 'success_message': success_message})
        else:
            logger.debug("Test debug form is invalid")
        return render(request, 'blog/contact.html', {'form': form , 'name': name, 'email': email, 'message': message})
    return render(request, 'blog/contact.html') 


def about(request):
    about_us = About_us.objects.first()
    if about_us is None or not about_us.content:
        about_us = "Default content"
    else:
        about_us = about_us.content
    return render(request, 'blog/about.html', {'About_us': about_us})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "your account has been created. you can log in now")
            return redirect("blog:login")
            
    return render(request, 'blog/register.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("user logged in")
                return redirect("blog:dashboard")
    return render(request, 'blog/login.html', {'form': form})


def dashboard(request):
    posttitle = "My Posts"
    all_post = Post.objects.filter(user_id=request.user)
    pagination = Paginator(all_post, 6)
    pag_number = request.GET.get('page')
    pages = pagination.get_page(pag_number)
    return render(request, 'blog/dashboard.html', {'pages': pages, 'posttitle': posttitle})


def logout(request):
    auth_logout(request)
    return redirect("blog:index")


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            #send email
            user = User.objects.get(email=email)
            #send email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            subject = 'Reset your password'
            message = render_to_string('blog/reset_password_email.html', { 
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            
            send_mail(subject, message, 'diludilux25@gmail.com', [email]) 
            messages.success(request, "Email has been sent")
        return render(request, 'blog/forgot_password.html', {'form': form})
            
    return render(request, 'blog/forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
                
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been changed")
                return redirect("blog:login")
            else:
                messages.error(request, "Link is invalid")
                
    return render(request, 'blog/reset_password.html', {'form': form})


def new_post(request):
    cato = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
        return redirect("blog:dashboard")
    return render(request, 'blog/new_post.html',{'category': cato, 'form': form})


def edit_post(request, post_id):
    cato = Category.objects.all()
    return render(request, 'blog/edit_post.html', {'category': cato})
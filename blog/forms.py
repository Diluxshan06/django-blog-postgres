from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Category, Post


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    message = forms.CharField(label='Message', required=True)

    
class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True)
    password_confirm = forms.CharField(label='Password Confirm', required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    
    def clean(self):
        clean_data = super().clean()
        
        email = clean_data.get('email')
        if email:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email does not exist.")
            
            
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', max_length=100, required=True)
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, required=True)
    
    def clean(self):
        cleaned_data = super().clean()
        
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
   
        
class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=200, required=True)
    content = forms.CharField(label='Content', required=True)
    category = forms.ModelChoiceField(label='Category', required=True, queryset=Category.objects.all())
    img = forms.ImageField(label='Image', required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img']
        
    def clean(self):
        cleaned_data = super().clean()
        
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        category = cleaned_data.get('category')
        
        if title and len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        if content and len(content) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long.")
        
    def save(self, commit=...):
        post = super().save(commit)
        cleaned_data = self.cleaned_data
        
        if cleaned_data.get('img'):
            post.img = cleaned_data.get('img')
        else:
            img = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
            post.img = img
        
        if commit:
            post.save()
        return post
        
from django.urls import reverse
from django.shortcuts import redirect


class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        #check user authenticated
        if request.user.is_authenticated:
            #set redirect paths 
            paths_to_redirect = [reverse('blog:login'), reverse('blog:register')]
            
            if request.path in paths_to_redirect:
                return redirect(reverse('blog:index'))
            
        respose = self.get_response(request)
        return respose
   
    
class RedirectUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        #check user authenticated
        if not request.user.is_authenticated:
            #set redirect paths 
            paths_to_redirect = [reverse('blog:dashboard')]
            
            if request.path in paths_to_redirect:
                return redirect(reverse('blog:login'))
            
        respose = self.get_response(request)
        return respose
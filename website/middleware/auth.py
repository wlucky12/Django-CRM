from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 允许访问的页面列表
        allowed_paths = ['/login/', '/register/']
        if request.path_info not in allowed_paths and not request.user.is_authenticated:
            return redirect('/login/')
        response = self.get_response(request)
        return response
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

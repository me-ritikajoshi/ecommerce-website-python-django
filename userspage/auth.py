from django.shortcuts import  redirect
from functools import wraps

#to check if the user is logged in or not
def unauthenticated_user(view_function):
    @wraps(view_function)
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('userspage:home')
        else:
            return view_function(request,*args,**kwargs)
    return wrapper_function

#to give access to admin if the request comes from the admin else access is given to normal page for normal user
def admin_only(view_function):
    @wraps(view_function)
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_staff:
            return view_function(request,*args,**kwargs)
        else:
            return redirect('userspage:home')
    return wrapper_function

            

from django.shortcuts import render, redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()

                for i in group:
                    if i.name in allowed_roles:
                        return view_func(request, *args, **kwargs)
                
            return render(request, 'permision_denied.html')

        return wrapper_func
    return decorator


def allowed_users_pk(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, news_pk, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()

                for i in group:
                    if i.name in allowed_roles:
                        return view_func(request, news_pk,*args, **kwargs)
                
            return render(request, 'permision_denied.html', status=403)

        return wrapper_func
    return decorator


def already_authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('main')
        return view_func(request, *args, **kwargs)
    return wrapper_func
from django.shortcuts import render

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
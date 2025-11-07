from functools import wraps

def clear_session_data(keys):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            for key in keys:
                if key in request.session:
                    del request.session[key]
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
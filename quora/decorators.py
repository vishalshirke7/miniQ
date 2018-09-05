from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#
# def myuser_login_required(f):
#     def wrap(request, *args, **kwargs):
#         # this check the session if userid key exist, if not it will redirect to login page
#         if 'userid' not in request.session.keys():
#             return HttpResponseRedirect("/mysite/login")
#         return f(request, *args, **kwargs)
#     wrap.__doc_ _ =f.__doc__
#     wrap.__name_ _ =f.__name__
#     return wrap


def myuser_login_required(fun):

    def wrap(request, *args, **kwargs):
        # this check the session if userid key exist, if not it will redirect to login page
        if 'user_id' not in request.session.keys():
            return HttpResponseRedirect(reverse('quora:login'))
        return fun(request, *args, **kwargs)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap
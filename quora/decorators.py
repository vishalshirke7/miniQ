from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def myuser_login_required(fun):

    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session.keys():
            return HttpResponseRedirect(reverse('quora:login'))
        return fun(request, *args, **kwargs)

    wrap.__doc__ = fun.__doc__
    wrap.__name__ = fun.__name__
    return wrap
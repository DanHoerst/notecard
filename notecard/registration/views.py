from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from notecard.registration.forms import *
from django.contrib.auth import authenticate, login, logout

def UserRegistration(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            new_user = form.save(data)
            return HttpResponseRedirect("/")
        return render_to_response("registration/register.html", {'form': form}, context_instance=RequestContext(request))
    else:
        form = UserCreateForm()
        return render_to_response("registration/register.html", {'form': form}, context_instance=RequestContext(request))
    
def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('registration/login.html', {'form': form}, context_instance=RequestContext(request))    
        else:
            return render_to_response('registration/login.html', {'form': form}, context_instance=RequestContext(request))    
    else:
        form = LoginForm()
        context = {"form": form}
        return render_to_response('registration/login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/auth/login/')

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from notecard.registration.forms import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
# String and Random used for password generator
import string
import random

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

def PasswordReset(request):
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            userEmail = form.cleaned_data['email']
            user = User.objects.get(email=userEmail)
            if user is not None:
                newPass = PasswordGenerator()
                user.set_password(newPass)
                user.save()
                site = 'notecard.herokuapp.com'
                from_add = 'admin@notecard.herokuapp.com'
                to = user.email
                subject = 'Notecards! requested password update'
                body = 'Please visit %s and login with your new password below.\n Your new password is: %s \n\n Please do not reply to this email. If you have any questions please email DHoerst1@gmail.com' % (site, newPass)
                send_mail(subject, body, from_add, [user.email], fail_silently=False)
                return render_to_response('registration/reset.html', context_instance=RequestContext(request))
            else:
                reset_error = 'No account with that email address currently exists'
                return render_to_response('registration/passwordreset.html', {'form': form, 'reset_error': reset_error}, context_instance=RequestContext(request))
        else:
            return render_to_response('registration/passwordreset.html', {'form': form,}, context_instance=RequestContext(request))
    else:
        form = ResetForm()
        context = {"form": form}
        return render_to_response('registration/passwordreset.html', context, context_instance=RequestContext(request))

def PasswordGenerator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

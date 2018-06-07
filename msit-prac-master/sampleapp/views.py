# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# from sampleapp.models import Room
from sampleapp.models import Room
from sampleapp.tokens import account_activation_token
from website.settings import EMAIL_HOST_USER
from .forms import SignUpForm

# Create your views here.

def index_view(request):
    template = 'sampleapp/index.html'
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:home'))

    context = {}
    signUpForm = SignUpForm()

    kwargs = request.session
    if kwargs:
        context['signup_errors'] = kwargs.pop('signup_errors', None)
        context['signin_error'] = kwargs.pop('signin_error', None)
        context['signin_username'] = kwargs.pop('signin_username', None)
        context['redirect_from'] = kwargs.pop('redirect_from', None)

        uname = kwargs.pop('signup_username', None)
        email = kwargs.pop('signup_email', None)
        fname = kwargs.pop('signup_fname', None)
        lname = kwargs.pop('signup_lname', None)

        if uname and email and fname and lname:
            signUpForm = SignUpForm(initial={
                'username': uname,
                'first_name': fname,
                'last_name': lname,
                'email': email,
            })

    context['signup_form'] = signUpForm

    return render(request, template, context)


def signup_view(request):
    '''
    Sign up functionality.
    :param request:
    :return:
    '''

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active = False
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('sampleapp:home'))

            # current_site = get_current_site(request)
            #
            # subject = 'Welcome to Ting! Thanks for signing up!'
            #
            # message = render_to_string('sampleapp/activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # # user.email_user(subject, message)
            #
            # send_mail(subject=subject,
            #           message=message,
            #           from_email=EMAIL_HOST_USER,
            #           recipient_list=[user.email,],
            #           fail_silently=False)
            # return HttpResponseRedirect(reverse('sampleapp:account_activation_sent'))
        else:
            # messages.error(request, form)
            username = form.data.get('username')
            email = form.data.get('email')
            fname = form.data.get('first_name')
            lname = form.data.get('last_name')

            request.session['signup_username'] = username
            request.session['signup_email'] = email
            request.session['signup_fname'] = fname
            request.session['signup_lname'] = lname

            for key in form.errors:
                messages.error(request, form.errors.get(key))
            return HttpResponseRedirect(reverse('sampleapp:index'))

    return HttpResponseRedirect(reverse('sampleapp:index'))


def login_view(request):
    if request.method == 'POST':
        # Correct login method.
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            # The redirect must be to the home page. Change this later.
            login(request, user)
            return HttpResponseRedirect(reverse('sampleapp:home'))
        else:
            # Mark the error and send it back. We're clearing out the password and keeping the username.
            request.session['signin_error'] = 'Incorrect username or password.'
            request.session['signin_username'] = uname
            request.session['redirect_from'] = 'login'
            return HttpResponseRedirect(reverse('sampleapp:index'))
    else:
        # Incorrect method of login. Might need to change this later.
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('sampleapp:index'))

        return HttpResponseRedirect(reverse('sampleapp:home'))


def about_view(request):
    return render(request, 'sampleapp/about.html')


@login_required(login_url='/music/login/')
def home_view(request):
    form = PasswordChangeForm(user=request.user)
    active_users = get_current_users(request)
    # print (active_users)

    # Get conversations
    my_conversations = []
    for obj in Room.objects.all():
        if obj.contains_user(request.user.id):
            # Sending data as a tuple.
            # The tuple will be (room name, room link)
            my_conversations.append((obj.get_room_name(request.user.id), obj.get_room_link(request.user.id)))

    context = {'change_pwd_form': form,
               'online_users': active_users,
               'my_conversations': my_conversations}
    return render(request, 'sampleapp/home.html', context)


@login_required(login_url='/music/login')
def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:login'))
    return render(request, 'sampleapp/profile.html', {'user': request.user})


@login_required(login_url='/music/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('sampleapp:index'))


@login_required(login_url='/music/login')
def change_pwd(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('sampleapp:index'))
        else:
            return render(request, "sampleapp/change_pwd.html", { 'change_pwd_form': form })
    else:
        return HttpResponseRedirect(reverse('sampleapp:home'))


def account_activation_sent(request):
    return render(request, 'sampleapp/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('sampleapp:index'))
    else:
        return render(request, 'sampleapp/account_activation_invalid.html')


def get_current_users(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        some_user = data.get('_auth_user_id', None)

        if some_user and int(some_user) != int(request.user.id):
            user_id_list.append(some_user)

    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


def chat_with(request, u):
    """
    Opens the chat window for a specific user.
    u is either 'all', or the ID of a user.
    :param request:
    :param u:
    :return:
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sampleapp:index'))

    # Can't chat with yourself
    if str(u) == str(request.user.id):
        return HttpResponseRedirect(reverse('sampleapp:error'))

    if u == 'all':
        # Global chat
        room, created = Room.objects.get_or_create(label='global')
        context = { 'chatting_with': 'Everyone' }
        return render_room(room, request, context)
    else:
        try:
            # Checking if the other user exists
            other_user = User.objects.get(id=u)

            # Get the room and render it
            room = get_room(request.user.id, u)
            chatting_with = other_user.first_name + ' ' + other_user.last_name if len(other_user.first_name) > 0 and len(other_user.last_name) > 0 else other_user.username

            context = { 'chatting_with': chatting_with }
            return render_room(room, request, context)
        except User.DoesNotExist:
            return render(request, 'sampleapp/error.html')


def error_view(request):
    return render(request, 'sampleapp/error.html')

def render_room(room, request, context):
    """
    Renders a chat room.
    :param room: Chat room object
    :param request: HTTP request object
    :return: Rendering of chat room.
    """
    msgs = room.messages.order_by('timestamp')
    # msgs = []
    # for msg in msgs:
        # unique_id = msg.timestamp.strftime("%Y-%m-%d%H:%M:%S")
        # msgs.append((msg, unique_id))
    context['room'] = room
    context['msgs'] = msgs
    context['username'] = request.user.username
    return render(request, 'sampleapp/room.html', context)


def get_room(this_id, other_id):
    """
    Get chat room for one-to-one chat. The Room label will either be <this_user>_<other_user> or
    <other_user>_<this_user>.
    :param this_id: ID of currently logged in user.
    :param other_id: ID of other user.
    :return: Appropriate room.
    """
    this_id = str(this_id)
    other_id = str(other_id)

    one = this_id + '_' + other_id
    two = other_id + '_' + this_id

    try:
        return Room.objects.get(label=one)
    except Room.DoesNotExist:
        try:
            return Room.objects.get(label=two)
        except Room.DoesNotExist:
            new_room = Room.objects.create(label=one)
            return new_room


'''
Not used. The relics of history (and editing and common sense).

class SignUpView(View):
    def get(self, request):
        return render(request, 'sampleapp/signup.html')

    def post(self, request):
        uname = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        newuser = User.objects.create_user(username=uname,
                                           email=email,
                                           password=pwd,
                                           first_name=fname,
                                           last_name=lname)
        newuser.save()

        return redirect('/music/')
        
        
class SignInView(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'sampleapp/signin.html')

        

    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')

        user = authenticate(username=uname, password=pwd)

        if user is not None:
            # Change this.
            return HttpResponseRedirect(reverse('sampleapp:profile', args=(user.get_username(),)))
        else:
            context = {'error': 'Username %s does not exist.' % uname}
            return render(request, 'sampleapp/signin.html', context)
            
        
class IndexView(TemplateView):
    template_name = 'sampleapp/index.html'

    def get_context_data(self, **kwargs):
        context = TemplateView().get_context_data(**kwargs)
        if self.request.user:
            context['user'] = self.request.user
        return context
        
        
def chat_room(request, label):
    room, created = Room.objects.get_or_create(label=label)
    msgs = reversed(room.messages.order_by('-timestamp')[:50])
    return render(request, 'sampleapp/room.html', {
        'room': room,
        'msgs': msgs,
        'username': request.user.username
    })
'''
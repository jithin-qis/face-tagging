from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, User, Following, Follower, Post, DefaultPic
from django.urls import reverse
from django.http import HttpResponseRedirect
from .code import blur_img, check_img
import os
from .models import Post
from django.core.mail import send_mail  


def index(request):
    form = UserLoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect(feed)
    if request.method == 'POST':
        if form.is_valid():
            email=request.POST.get('email')
            username = User.objects.get(email=email).username
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(feed)
    return render(request, 'core/login.html', {'form':form,})


@login_required
def blurid(request, id=None):
    pro_pic = os.path.join('media', request.user.profile.profile_photo.name)
    p = Post.objects.get(id=id)
    print('post_pic:', os.path.join('media', p.post_picture.name), 'pro_pic:',
          os.path.join('media', request.user.profile.profile_photo.name))
    blur_img(os.path.join('media', p.post_picture.name), pro_pic)

    return redirect(feed)

@login_required
def blur(request):
    inp = os.path.join('media', request.user.profile.profile_photo.name)
    for posts in Post.objects.all():
        blur_img(os.path.join('media', posts.post_picture.name), inp)
    return redirect(feed)


def mailindex(request):
    if request.user.is_authenticated: 
        logout(request)
    # return render(request,'core/index.html')
    return render(request, 'core/login.html')



import random
def profile(request, username=None):
    username = request.user.username

    c = True
    try:
        p_form = UpdateProfileForm( request.POST or None, request.FILES or None,instance=request.user.profile)
        print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
    except:
        p_form = UpdateProfileForm(request.POST, request.FILES)
        print('PPPPPPPPPPPPPPPP')
        c = False

    if request.method == 'POST':
        print('------------------------------POST')
        u_form = UpdateUserForm(request.POST, instance=request.user)
        # p_form = UpdateProfileForm(request.POST, request.FILES)
        # if c:
        #     p_form = UpdateProfileForm(instance=request.user.profile)
        #     print('IOIOIOIOIOIOIOIOIOIOI')
        # else:
        #     p_form = UpdateProfileForm(request.POST, request.FILES)
        if u_form.is_valid() or p_form.is_valid():
            print('-------------------valid')
            try:
                u_form.save()
            except:
                pass
            if c:
                # instance = Profile.objects.get(user=request.user)
                # instance.profile_picture = request.FILES['profile_photo']
                # instance.save()
                # print('===========Here')
                p_form.save()
            else:
                instance = p_form.save(commit=False)
                instance.user = request.user
                instance.save()
                print('__________________HERRRRR')

            messages.success(request, f'Your Profile has been updated!')
            url = reverse('profile', kwargs={'username': username})
            return redirect(url)
        elif p_form.is_valid():
            print('-----------------pform')
    else:
        if username == request.user.username:
            u_form = UpdateUserForm(instance=request.user)
            # p_form = UpdateProfileForm(instance=request.user.profile)
            p_form = UpdateProfileForm()
            post_form = CreatePost()
            person = User.objects.get(username=username)

            context = {
                'u_form': u_form,
                'p_form': p_form,
                'post_form': post_form,
                'person': person,
                'allposts':Post.objects.all()

            }
        else:
            person = User.objects.get(username=username)
            already_a_follower = 0
            for followers in person.follower_set.all():
                if (followers.follower_user == request.user.username):
                    already_a_follower = 1
                    break

            if already_a_follower == 1:
                context = {
                    'person': person,


                }
            else:
                context = {
                    'person': person,
                    'f': 1,

                }
        comment_form = CreateComment()
        context.update({'comment_form': comment_form, 'ts':random.randint(100, 136846)})
    # print(context)
    return render(request, 'core/profile.html', context)





class UserFormView(View):
    form_class = UserForm
    template_name = 'core/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, f'Account created for {username}!')
                    return redirect('core:index')

        return render(request, self.template_name, {'form': form})


def followweb(request, username):
    if request.user.username != username:
        if request.method == 'POST':
            disciple = User.objects.get(username=request.user.username)
            leader = User.objects.get(username=username)

            leader.follower_set.create(follower_user=disciple)
            disciple.following_set.create(following_user=leader)
            url = reverse('profile', kwargs={'username': username})
            return redirect(url)


def unfollowweb(request, username):

    if request.method == 'POST':
        disciple = User.objects.get(username=request.user.username)
        leader = User.objects.get(username=username)

        leader.follower_set.get(follower_user=disciple).delete()
        disciple.following_set.get(following_user=leader).delete()
        url = reverse('profile', kwargs={'username': username})
        return redirect(url)


def welcome(request):
    url = reverse('profile', kwargs={'username': request.user.username})
    return redirect(url)

def send_emails(emails):
        send_mail(
        'Your photo detected',
        '',
        'questpython@gmaail.com',
        emails,
        html_message=f'''
            <h4>Hi, Your photo has been found on a phtoto uploaded by someone. Please use the link below to login and review</h4>
        <h3>
        <a href="http://127.0.0.1:8000/mailindex/">
        <button style="  background-color: #4CAF50; /* Green */border: none;color: white;padding: 10px;text-align: center;text-decoration: none;display: inline-block;font-size: 16px; margin: 4px 2px;cursor: pointer;border-radius: 12px;">Click here</button>
        </a>to login
        </h3>
        ''')

def postweb(request, username):
    if request.method == 'POST':       
        post_form = CreatePost(request.POST, request.FILES)
        if post_form.is_valid():
            post_text = post_form.cleaned_data['post_text']
            post_picture = request.FILES.get('post_picture')
            request.user.post_set.create(
                post_text=post_text, post_picture=post_picture)
            max_id = max([i.id for i in Post.objects.all()])
            post_pic = Post.objects.get(id=max_id)
            post_pic = os.path.join(os.getcwd(),'media',post_pic.post_picture.name)
            pro_pics = []
            f = []
            for i in User.objects.all():
                try:
                    pro_pics=os.path.join(os.getcwd(),'media',i.profile.profile_photo.name)
                    result =  check_img(post_pic, pro_pics)
                    s = 'D:\QUEST\PROJECTS\face_tagging\mysite\media\profile_photos/'
                    s = result.split('media')[1][1:]
                    f.append(s)
                except:
                    pass
            emails = []
            for i in User.objects.all():
                try:
                    if i.profile.profile_photo.name in f:
                        emails.append(i.email)
                except:
                    pass
            print(emails)
            send_emails(emails)

            # pro_pics = [os.path.join(os.getcwd(),'media',i) for i in pro_pics]
            # # print(post_pic)
            # for i in pro_pics:
            #     result =  check_img(post_pic, i)
            #     s = 'D:\QUEST\PROJECTS\face_tagging\mysite\media\profile_photos/'
            #     s = result.split('media')[1]
            #     print(s)


                    # print(f'Found this face: {i}')
                # else:
                #     print(f'Cannot find this face: {i}')
            messages.success(request, f'You have successfully posted!')
    url = reverse('profile', kwargs={'username': username})
    return redirect(url)


def commentweb(request, username, post_id):
    if request.method == 'POST':

        comment_form = CreateComment(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            user = User.objects.get(username=username)
            post = user.post_set.get(pk=post_id)
            post.comment_set.create(
                user=request.user, comment_text=comment_text)

            messages.success(request, f'Your Comment has been posted')

    url = reverse('profile', kwargs={'username': username})
    return redirect(url)


def feed(request):
    if request.user.is_authenticated:
        return redirect(welcome)
    # return render(request,'core/index.html')
    return render(request, 'core/login.html')

    # post_all = Post.objects.order_by('created_at').reverse()
    #
    # comment_form = CreateComment()
    # context = {
    #     'post_all': post_all,
    #     'comment_form': comment_form,
    # }
    # return render(request, 'core/feed.html', context)


from .click import clickpic as cp


def clickfun(request):
    try:
        form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    except:
        form = UpdateProfileForm(request.POST or None, request.FILES or None)

    # user, profile_photo, status_info
    try:
        p = Profile.objects.get(user=request.user)
        cp(os.path.join('media', request.user.profile.profile_photo.name))
    except:
        i = form.save(commit=False)
        i.user = request.user
        i.status_info = ' '
        i.profile_photo = DefaultPic.objects.all()[0].pic
        i.save()
        p = Profile.objects.get(user=request.user)
        cp(os.path.join('media', request.user.profile.profile_photo.name))
    return redirect(welcome)
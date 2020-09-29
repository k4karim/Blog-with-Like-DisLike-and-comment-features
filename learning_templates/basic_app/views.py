# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Comment,UserProfileInfo,Upvotes,Downvotes
from basic_app.forms import PostForm,CommentForm,UserForm,UserProfileInfoForm

import csv,json
import io
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'basic_app/post_list.html', {'posts': posts})

def index(request):
    return render(request,'basic_app/index.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    number_of_likes = post.upvote.all().count()
    number_of_dislikes = post.downvote.all().count()

    if request.method=="POST":

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Thank You for Your Comment.It will be publicly visible once post admin approve it', extra_tags='alert')
            return redirect('basic_app:post_detail', pk=post.pk)

    else:
         form = CommentForm()
    return render(request, 'basic_app/post_detail.html', {'post': post,'form': form,'number_of_likes':number_of_likes,'number_of_dislikes':number_of_dislikes})

##def post_detail(request, pk):
##    post = get_object_or_404(Post,pk=pk)
##    return render(request, 'basic_app/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            #post.published_date=timezone.now()
            post.save()
            messages.success(request, 'You have succesfully added post please publish it manually by clicking Publish button', extra_tags='alert')
            return redirect('basic_app:post_detail',pk=post.pk)
    else:
         form=PostForm()
    return render(request, 'basic_app/post_new.html', {'form': form})


@login_required
def post_edit(request,pk):

    post=get_object_or_404(Post,pk=pk)
    if post.author == request.user:
        if request.method=="POST":
            form=PostForm(request.POST, instance=post)
            if form.is_valid():
                post=form.save(commit=False)
                post.author=request.user
                post.published_date=timezone.now()
                post.save()
                messages.success(request, 'You have succesfully updated post', extra_tags='alert')
                return redirect('basic_app:post_detail',pk=post.pk)
        else:
             form=PostForm(instance=post)
        return render(request, 'basic_app/post_edit.html', {'form': form,'post':post})
    else:
        messages.warning(request, "You cannot edit posts")
        return redirect('basic_app:post_detail',pk=post.pk)





@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True,author=request.user).order_by('published_date')
    #if posts.author == request.user:
    return render(request, 'basic_app/post_draft_list.html', {'posts': posts})



def myposts_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(),author=request.user).order_by('published_date')

    #if posts.author == request.user:
    return render(request, 'basic_app/myposts_list.html', {'posts': posts})


@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if post.author == request.user:
        post.publish()
        messages.success(request, 'You have succesfully published post.Now it is Publicly Visible', extra_tags='alert')
        return redirect('basic_app:post_detail',pk=pk)
    return redirect('basic_app:post_detail',pk=pk)


@login_required
def unpost_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.published_date='YYYY-MM-DD HH:MM:ss'
    post.save()
    messages.success(request, 'You have succesfully moved Your Post to Draft.Now it is not Publicly Visible', extra_tags='alert')
    return redirect('basic_app:post_detail',pk=pk)

@login_required
def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'You have succesfully Deleted post.Now it is deleted permanantly ', extra_tags='alert')
        return redirect('basic_app:post_list')
    return redirect('basic_app:post_list')




@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if comment.post.author == request.user or request.user.is_superuser:
        comment.approve()
        messages.success(request, 'You have succesfully approved comment.Now it is visible to public ', extra_tags='alert')
        return redirect('basic_app:post_detail',pk=comment.post.pk)
    else:
        messages.warning(request, "You cannot edit posts")
        return redirect('basic_app:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if comment.post.author == request.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, 'You have succesfully Deleted comment.Now it is deleted permanantly ', extra_tags='alert')
        return redirect('basic_app:post_detail',pk=comment.post.pk)

@login_required
def uncomment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if comment.post.author == request.user or request.user.is_superuser:
        comment.approved_comment=False
        comment.save()
        return redirect('basic_app:post_detail',pk=comment.post.pk)






def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():


            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:

                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})



def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:

            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'registration/login.html', {})


def server_error(request):
    return redirect('user_login')



def profilepagelist(request):
    users = UserProfileInfo.objects.all()
    return render(request, 'basic_app/profilepagelist.html', {'users': users})



def profilepage(request, pk):
    usersss = get_object_or_404(UserProfileInfo, pk=pk)

    return render(request, 'basic_app/profilepage.html', {'usersss': usersss})



@login_required
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.upvote.filter(author=request.user).exists() or post.downvote.filter(author=request.user).exists():

        messages.error(request, 'You have Already voted for this post', extra_tags='alert')


    else:
        newlike = Upvotes.objects.create(author=request.user, post=post)
        messages.success(request, 'Thank You for upvoting  this post', extra_tags='alert')

    return redirect('basic_app:post_detail',pk=pk)

@login_required
def dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)


    if post.upvote.filter(author=request.user).exists() or post.downvote.filter(author=request.user).exists():
        messages.error(request, 'You have Already voted for this post', extra_tags='alert')
    else:
        newdislike = Downvotes.objects.get_or_create(author=request.user, post=post)
        messages.success(request, 'Thank You for downvoting  this post', extra_tags='alert')

    return redirect('basic_app:post_detail',pk=pk)




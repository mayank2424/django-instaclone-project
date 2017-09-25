# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from time import timezone
from django.shortcuts import render, redirect
from models import UserModel, SessionToken,PostModel
from forms import SignUpForm , LoginForm,PostForm
from django.contrib.auth.hashers import make_password , check_password
from myproject.settings import BASE_DIR
from imgurpython import ImgurClient


YOUR_CLIENT_ID= "047cacc8f25b368"
YOUR_CLIENT_SECRET="6db406c67ee27513b6ead9f7ef7136d19d197de2"

# Create your views here.
def signup_view(request): #here we have made signup_view function for sigining up on our website
    if request.method == "POST":   #here we have used post method for requesting
        form = SignUpForm(request.POST)   #form is a library defined in django
        if form.is_valid():  #if form is valid means agar isme koi validation error nh hain to it will return cleaned data
            username=form.cleaned_data['username']   # cleaned data means data with no error
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user = UserModel(name=name,password=make_password(password),email=email, username=username)
            user.save()   # here we have saved all user details
            return render(request, 'success.html')

    else:
     form = SignUpForm()
    return render(request, 'index.html', {'form': form})

def login_view(request):
    response_request={}
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username=  form.cleaned_data.get('username')
            password=  form.cleaned_data.get('password')

            user= UserModel.objects.filter(username=username).first()
            if user:
               if not check_password(password, user.password):
                   response_request['message']= "invalid password"

               else:
                   token = SessionToken(user=user)
                   token.create_token()
                   token.save()

                   response= redirect('/feed/')
                   response.set_cookie(key= 'session_token' , value= token.session_token)
                   return response

    else:
        form= LoginForm()

    response_request['form']= form
    return render(request, 'login.html', response_request)

def post_view(request):
    user= check_validation(request)
    if user:
      if request.method== 'POST':
            form=PostForm(request.POST, request.FILES)
            if form.is_valid():
                 image=form.cleaned_data.get('image')
                 caption=form.cleaned_data.get('caption')
                 post=PostModel(user=user, image=image, caption=caption)
                 post.save()

                 path=str(BASE_DIR + '/' + post.image.url)

                 client=ImgurClient(YOUR_CLIENT_ID, YOUR_CLIENT_SECRET)
                 post.image_url=client.upload_from_path(path,anon=True)['link']
                 post.save()

                 return redirect('/feed/')
      else:
           form =PostForm()
      return render(request, 'post.html', {'form' :form })
    else:
        return redirect('/login/')






def check_validation(request):
    if request.COOKIES.get('session_token'):
        session= SessionToken.objects.filter(session_token = request.COOKIES.get('session_token')).first()
        if session:
            # time_to_live=session.created_on + timedelta(days=1)
            # if time_to_live> timezone.now():
            if True:
                return session.user
    else:
        return None
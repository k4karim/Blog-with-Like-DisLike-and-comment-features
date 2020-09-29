from django import forms
from django.contrib.auth.models import User

from basic_app.models import Post,Comment,UserProfileInfo

class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('title','text',)

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control',"placeholder": "Enter Post title",'required':True,}),
            'text':forms.Textarea(attrs={'class':'form-control z-depth-1',"placeholder": "Write Post here",'required':True,}),

            }


class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('text',)

        widgets={
            'text':forms.Textarea(attrs={'class':'form-control z-depth-1 input-sm',"placeholder": "write comment here"}),


            }





class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',"placeholder": "Enter Your Password",'required':True,}))

    class Meta():
        model = User
        fields = ('username','email','password')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control',"placeholder": "Enter Your UserName",'required':True,}),
            'email':forms.EmailInput(attrs={'class':'form-control',"placeholder": "Enter Your Email",'required':True,}),

            }

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

        widgets={
            'profile_pic':forms.FileInput(attrs={'class':'form-control-file',"placeholder": "Enter Your UserName"}),


            }

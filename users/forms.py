from django import forms
from users.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','password')


    def save(self,commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save() 
        
        #send_email
        if user.email:
            send_mail(
            'Welcome to goodreads clone',
            f'Hi {user.username}, we are happy to ann ounce our website is good enough',
            'adam.lion077@gmail.com',
            [user.email],
            fail_silently=False

            )
        return user



    # def __init__(self, *args, **kwargs):
    #     super(UserCreateForm, self).__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email','profile_picture')
        































# class UserCreateForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     email = forms.EmailField()
#     first_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     password = forms.CharField(max_length=128)


#     def save(self):
#         username = self.cleaned_data['username']
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']

#         user = User.objects.create(
#             username=username,
#             first_name = first_name,
#             last_name = last_name,
#             email = email
#             )
#         user.set_password(password)
#         user.save()        
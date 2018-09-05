from django import forms

from quora.random_string_generator import random_string_generator_c
from .models import User, Question, Answers


class SignupForm(forms.Form):

    fname = forms.CharField(label="First Name", required=True)
    lname = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(label="Password", required=True)
    repassword = forms.CharField(label="Re-type Password", required=True)

    class Meta:
        model = User

    def clean_email(self):
         email = self.cleaned_data.get('email')
         try:
             match = User.objects.get(email=email)
         except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
         raise forms.ValidationError('This email address is already in use.')

    def clean_repassword(self):
        psw = self.cleaned_data.get('password')
        repsw = self.cleaned_data.get('repassword')
        if psw != repsw:
            raise forms.ValidationError("Password doesn't match!")
        return self.cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(label="Email/Username", required=True)
    password = forms.CharField(label="Password", required=True)

    class Meta:
        model = User

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        ranstrng = random_string_generator_c()
        userpasw = ranstrng.hash_password(password)

        try:
            user = User.objects.get(email=username)
            if user.password != userpasw:
                raise forms.ValidationError("Sorry, wrong username or password !")
        except User.DoesNotExist:
                raise forms.ValidationError("Invalid Login")
        return self.cleaned_data


class QuestionForm(forms.Form):

    question = forms.CharField(label="What's on your mind", required=True)

    class Meta:
        model = Question


class AnswerForm(forms.Form):

    answer = forms.CharField(label="", required=True)

    class Meta:
        model = Answers

# widget = forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "20", })
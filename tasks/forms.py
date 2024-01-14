
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Task

class RegistroUserForm(UserCreationForm):

    model=User
    fields=('username','password1','password2')
    def __init__(self, *args, **kwargs) -> None:
        super(RegistroUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'

        self.fields['password2'].widget.attrs['class']='form-control'

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','important']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Write your title'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Write your description'}),

            'important':forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
        }

        
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from statpools import models

class CreateStatPoolForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'name-input'}), label="")

    class Meta():
        model = models.StatPool
        fields = ('name')

class CreateStatPoolCategoryForm(forms.Form):
    gameSelectedInput = forms.CharField()
    playerSelectedInput = forms.CharField()
    statSelectedInput = forms.CharField()

    class Meta():
        model = models.StatPoolCategory
        fields = ('name')

class AddUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username).first()
        statpool = self.request.POST['statpoolid']
        if not new:
            raise ValidationError("No user with that name exists")

        isadded = models.StatPoolUser.objects.filter(user_id_id=new.id, stat_pool_id_id=statpool).first()
        if isadded:
            raise ValidationError("User has already been added")
        return username

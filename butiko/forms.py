from django import forms
from django.contrib.auth.models import User
from .models import Item, ItemList

class ItemForm(forms.ModelForm):
    
    class Meta:
        model  = Item
        fields = ('title', 'store', 'number', 'price',)

class ItemListForm(forms.ModelForm):

    class Meta:
        model  = ItemList
        fields = ('title',)

class UserForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model   = User
        widgets = {'password': forms.PasswordInput(),}
        fields  = ('username', 'first_name', 'last_name', 'email', 'password')

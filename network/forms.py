from django import forms

class NewPostForm(forms.Form):
    post = forms.CharField(label="New Post")
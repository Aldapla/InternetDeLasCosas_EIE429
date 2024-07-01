from django import forms
from .models import Post, Comentario

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'seccion']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

class VerificarCapitalForm(forms.Form):
    capital_id = forms.IntegerField(widget=forms.HiddenInput)
    respuesta = forms.CharField(max_length=100)
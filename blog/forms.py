from .models import Comment, Cv, Post
from django import forms

class CommentForm(forms.ModelForm):
	
	class Meta:
		model = Comment
		fields = ('author', 'text',)
		
class CvForm(forms.ModelForm):
	
	class Meta:
		model = Cv
		fields = ('summary', 'education', 'experience', 'other')
		
class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ('title', 'text',)

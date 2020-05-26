from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Comment(models.Model):
	author = models.CharField(max_length=50)
	created_date = models.DateTimeField(default=timezone.now)
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	
	def __str__(self):
		return self.text
		
class Cv(models.Model):
	summary = models.TextField()
	education = models.TextField()
	experience = models.TextField()
	other = models.TextField()
	
	def save(self, *args, **kwargs):
		if not self.pk and Cv.objects.exists():
			raise ValidationError('You cannot create more than one CV')
		return super(Cv, self).save(*args, **kwargs)
		
	def __str__(self):
		return self.summary
		
class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	text = models.TextField()
	title = models.CharField(max_length=200)
	
	def publish(self):
		self.published_date = timezone.now()
		self.save()
	
	def __str__(self):
		return self.title

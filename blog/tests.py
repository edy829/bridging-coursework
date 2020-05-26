from blog.forms import CvForm
from blog.models import Cv
from blog.views import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

class CvTest(TestCase):
	
	# Helper method for logging in
	def login(self):
		self.client.force_login(User.objects.get_or_create(username='testuser')[0])
	
	# Helper method for creating a new CV
	def new_cv(self):
		return self.client.post('/cv/new/', data={
			'summary': 'Student',
			'education': 'Birmingham',
			'experience': 'Intel',
			'other': 'None'
		})
		
	# Helper method for editing a CV
	def edit_cv(self):
		return self.client.post('/cv/1/edit/', data={
			'summary': 'Enthusiastic student',
			'education': 'University of Birmingham',
			'experience': 'Intel and Qualcomm',
			'other': 'I like dogs'
		})
		
	# Helper method for removing a CV
	def remove_cv(self):
		return self.client.get('/cv/1/remove/')
		
	###########################################################################
	#                                                                         #
	#                                  Tests                                  #
	#                                                                         #
	###########################################################################
		
	# CV homepage tests:
	def test_cv_homepage_returns_correct_template(self):
		response = self.client.get('/cv/', follow=True)
		
		self.assertTemplateUsed(response, 'cv/cv_none.html')
		
	# New CV tests:
	def test_new_cv_returns_correct_template(self):
		self.login()
		
		response = self.client.get('/cv/new/')
		
		self.assertTemplateUsed(response, 'cv/cv_new.html')
		
	def test_can_save_a_new_cv(self):
		self.login()
		self.new_cv()
		
		cv = Cv.objects.first()
		
		self.assertEqual(cv.summary, 'Student')
		self.assertEqual(cv.education, 'Birmingham')
		self.assertEqual(cv.experience, 'Intel')
		self.assertEqual(cv.other, 'None')
		
	def test_redirects_after_creating_a_cv(self):
		self.login()
		
		response = self.new_cv()
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/cv/1/')
		
	def test_cv_homepage_displays_new_cv_text(self):
		self.login()
		self.new_cv()
		
		response = self.client.get('/cv/', follow=True)
		
		self.assertIn('Student', response.content.decode())
		self.assertIn('Birmingham', response.content.decode())
		self.assertIn('Intel', response.content.decode())
		self.assertIn('None', response.content.decode())
		
	def test_cannot_create_more_than_one_cv(self):
		self.login()
		self.new_cv()
		
		with self.assertRaises(ValidationError):
			self.new_cv()
			
	# Edit CV tests:
	def test_edit_cv_returns_correct_template(self):
		self.login()
		self.new_cv()
		
		response = self.client.get('/cv/1/edit/')
		
		self.assertTemplateUsed(response, 'cv/cv_edit.html')
		
	def test_can_save_an_edited_cv(self):
		self.login()
		self.new_cv()
		self.edit_cv()
		
		cv = Cv.objects.first()
		
		self.assertEqual(cv.summary, 'Enthusiastic student')
		self.assertEqual(cv.education, 'University of Birmingham')
		self.assertEqual(cv.experience, 'Intel and Qualcomm')
		self.assertEqual(cv.other, 'I like dogs')
		
	def test_redirects_after_editing_a_cv(self):
		self.login()
		self.new_cv()
		
		response = self.edit_cv()
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/cv/1/')
		
	def test_cv_homepage_displays_edited_cv_text(self):
		self.login()
		self.new_cv()
		self.edit_cv()
		
		response = self.client.get('/cv/', follow=True)
		
		self.assertIn('Enthusiastic student', response.content.decode())
		self.assertIn('University of Birmingham', response.content.decode())
		self.assertIn('Intel and Qualcomm', response.content.decode())
		self.assertIn('I like dogs', response.content.decode())
		
	# Remove CV tests:
	def test_can_remove_a_cv(self):
		self.login()
		self.new_cv()
		self.remove_cv()
		
		cvs = Cv.objects.all()
		
		self.assertFalse(cvs)
		
	def test_redirects_after_removing_a_cv(self):
		self.login()
		self.new_cv()
		
		response = self.remove_cv()
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/cv/')
		
	def test_homepage_no_longer_displays_text_of_removed_cv(self):
		self.login()
		self.new_cv()
		self.remove_cv()
		
		response = self.client.get('/cv/', follow=True)
		
		self.assertNotIn('Student', response.content.decode())
		self.assertNotIn('Birmingham', response.content.decode())
		self.assertNotIn('Intel', response.content.decode())
		self.assertNotIn('None', response.content.decode())

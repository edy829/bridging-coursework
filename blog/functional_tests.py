from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class CvTest(unittest.TestCase):
	
	home = 'http://127.0.0.1:8000/'
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
	def test_create_edit_remove_cv(self):
		#######################################################################
		#                                                                     #
		#                           Create CV test                            #
		#                                                                     #
		#######################################################################
		
		# Erik wants to create a CV. He goes to the website's login page
		self.browser.get(self.home + 'accounts/login/')
		
		# He sees two input fields: one for his username and one for his
		# password
		usr = self.browser.find_element_by_name('username')
		pwd = self.browser.find_element_by_name('password')
		
		# He enters his username and password
		usr.send_keys('erik')
		pwd.send_keys('erikspassword')
		
		# And submits the form
		btn = self.browser.find_element_by_tag_name('button')
		btn.submit()
		time.sleep(1)
		
		# He creates a new CV
		self.browser.get(self.home + 'cv/new/')
		
		# He sees four input fields: 'Summary', 'Education', 'Experience', and
		# 'Other'
		inputs = self.browser.find_elements_by_tag_name('textarea')
		summ = inputs[0]
		edu = inputs[1]
		exp = inputs[2]
		other = inputs[3]
		
		# He enters 'Student' into the summary secion, 'Birmingham' into the
		# education section, 'Intel' into the experience section, and 'None'
		# into the other section
		summ.send_keys('Student')
		edu.send_keys('Birmingham')
		exp.send_keys('Intel')
		other.send_keys('None')
		
		# And submits the form
		btn = self.browser.find_element_by_tag_name('button')
		btn.submit()
		time.sleep(1)
		
		# He is redirected to the CV page, which now displays 'Student' in the
		# summary section, 'Birmingham' in the education section, 'Intel' in 
		# the experience section, and 'None' in the other section
		txts = self.browser.find_elements_by_tag_name('p')
		summ = txts[0]
		edu = txts[1]
		exp = txts[2]
		other = txts[3]
		
		self.assertEqual(summ.text, 'Student')
		self.assertEqual(edu.text, 'Birmingham')
		self.assertEqual(exp.text, 'Intel')
		self.assertEqual(other.text, 'None')
		
		# He takes note of the primary key displayed in the website's URL, as
		# he thinks this will come in handy later
		pk = self.browser.current_url.rsplit('/')[4]
		
		#######################################################################
		#                                                                     #
		#                            Edit CV test                             #
		#                                                                     #
		#######################################################################
		
		# Erik realises he made a mistake when creating his CV, so goes to edit
		# his newly created CV
		self.browser.get(self.home + 'cv/' + pk + '/edit/')
		
		# He clears the education section and enters 'University of Birmingham'
		edu = self.browser.find_elements_by_tag_name('textarea')[1]
		edu.clear()
		edu.send_keys('University of Birmingham')
		
		# And submits the form
		btn = self.browser.find_element_by_tag_name('button')
		btn.submit()
		time.sleep(1)
		
		# He is redirected to the CV page, which now displays 'University of
		# Birmingham' in the education secion.
		edu = self.browser.find_elements_by_tag_name('p')[1]
		self.assertEqual(edu.text, 'University of Birmingham')
		
		#######################################################################
		#                                                                     #
		#                           Delete CV test                            #
		#                                                                     #
		#######################################################################
		
		# Erik no longer wants to display his CV on his website, so goes to
		# remove the CV he has created
		self.browser.get(self.home + 'cv/' + pk + '/remove/')
		
		# He is redirected to the CV page, which now no longer displays any of
		# the text he had input previously
		txts = self.browser.find_elements_by_tag_name('p')
		
		self.assertNotIn('Student', [txt.text for txt in txts])
		self.assertNotIn('University of Birmingham', [txt.text for txt in txts])
		self.assertNotIn('Intel', [txt.text for txt in txts])
		self.assertNotIn('None', [txt.text for txt in txts])
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')

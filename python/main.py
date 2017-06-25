#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import cgi
import cgitb; cgitb.enable()
from google.appengine.ext import ndb



class MainPage(webapp2.RequestHandler):
    def get(self):
    		self.response.headers['Content-Type'] = 'text/html'
    		self.response.write("""<head><title>Merge word</title></head>""")
    		self.response.write("""<form>First word :<br>
        	<input type='text' name=first_word><br>Second word :<br>
        	<input type='text' name=second_word><br>
        	<input type='submit'></form>""")
        	merge_word=""
        	first_word=self.request.get("first_word")
        	second_word=self.request.get("second_word")

        	l_first_word=len(first_word)
        	l_second_word=len(second_word)
        	if l_second_word>l_first_word :
        		l=l_first_word
        	else:
        		l=l_second_word
        	for i in range(l):
 	   		merge_word+=(first_word[i])
 	   		merge_word+=(second_word[i])


 	   	if l==l_first_word:
 	   		merge_word+=second_word[l:]
 	   	else:
 	   		merge_word+=first_word[l:]

 	   	if merge_word!="":
 	   		self.response.write(merge_word)
 	



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

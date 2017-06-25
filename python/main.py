#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
import cgi
import cgitb; cgitb.enable()
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import urllib,json

 
class MergeWord(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("""<head><title>Merge Word</title></head>""")
        self.response.write("""
                <style>
                .content{
                    max-width: 500px;
                    margin: auto;
                }
                </style>
                <body bgcolor="#ffff99">
                <div class="content">
                <font size=150><b>Merge Word</b></font>
                <form>First word :<br>
            <input type='text' name="first_word"><br>Second word :<br>
            <input type='text' name="second_word"><br>
            <input type='submit'></form>
                </div>
                </body>
            """)

        merge_word=""
        first_word=self.request.get("first_word")
        second_word=self.request.get("second_word")

        l_first_word=len(first_word)
        l_second_word=len(second_word)
        l=min(l_first_word,l_second_word)
        for i in range(l):
            merge_word+=(first_word[i])
            merge_word+=(second_word[i])


        if l==l_first_word:
            merge_word+=second_word[l:]
        else:
            merge_word+=first_word[l:]

        if merge_word!="":
            self.response.out.write("""
                <div class="content">
                <font size=100><b>%s</b></font>
                </div>
                """%merge_word)
 	
class Transfer(webapp2.RequestHandler):
    def get(self):

        url='alice.fantasy-transit.appspot.com/net?format=json'
        response=urllib.urlopen(url)
        data=json.loads(response.read())
        self.response.write(data)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("""<head><title>Transfer</title></head>""")
        self.response.write("""
                <style>
                .content{
                    max-width: 500px;
                    margin: auto;
                }
                </style>
                <body bgcolor="#ffff99">
                <div class="content">
                <font size=150><b>Transfer</b></font>
                
                </div>
                </body>
            """)

app = webapp2.WSGIApplication([
    ('/MergeWord', MergeWord),('/Transfer',Transfer)
], debug=True)

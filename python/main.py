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
    def print_path(self,path):
        if path=="Not found path":
            self.response.out.write("""
                <font size=100>Not found path</font>
                """)
        for node in path:
            self.response.out.write("""
                <font size=100>>>> ((%s)) %s </font><br>
                """%(node[1],node[0]))
    def bfs(self,data,start,end):
        q=[]
        visited=[]
        q.append([(start,"")])
        visited.append(start)
        while(q):
            path=q.pop(0)
            node=path[-1][0]

            if node==end:
                return path

            for line in data:
                if node in line['Stations']:
                    index=line['Stations'].index(node)

                    if index!=0:
                        pre_node=line['Stations'][index-1]
                        if pre_node not in visited:
                            visited.append(pre_node)
                            new_path=list(path)
                            new_path.append((pre_node,line['Name']))
                            q.append(new_path)

                    if index!=len(line['Stations'])-1:
                        next_node=line['Stations'][index-1]
                        if next_node not in visited:
                            visited.append(next_node)
                            new_path=list(path)
                            new_path.append((next_node,line['Name']))
                            q.append(new_path)

        return "Not found path"

    def get_world(self):
        self.response.write("""
            <br>Select world :
            <form>
            <select name="world">
            <option>%s</option>
            <option>%s</option>
            <option>%s</option>
            <option>%s</option>
            <option>%s</option>
            </select><br><br>
            <input type="submit" method="post" value="Change world"></input>
            </form>
            <br><br>
            """%("Alice","Pokemon","Nausicaa","Lord of the ring","Tokyo"))
        world=self.request.get("world")
        world_url={"Alice":"http://alice.fantasy-transit.appspot.com/net?format=json"
        ,"Pokemon":"http://pokemon.fantasy-transit.appspot.com/net?format=json"
        ,"Nausicaa":"http://nausicaa.fantasy-transit.appspot.com/net?format=json"
        ,"Lord of the ring":"http://lotr.fantasy-transit.appspot.com/net?format=json"
        ,"Tokyo":"http://fantasy-transit.appspot.com/net?format=json"}
        if world!="":
            response=urllib.urlopen(world_url[world])
        else:
            response=urllib.urlopen(world_url["Alice"])
        data=json.loads(response.read())
        return data

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write("""<head><title>Transfer</title></head>""")
        self.response.write("""
                <style>
                .content{
                    max-width: 500px;
                    margin: auto;
                }
                </style>
                <body bgcolor="#99ffff">
                <div class="content">
                <font size=150><b>Transfer</b></font>
                
              
               
            """)
        data=self.get_world()
        towns=[]
        for line in data:
            for town in line['Stations']:
                if town not in towns:
                    towns.append(town)

        
        
        self.response.write("""
    
            <form>
                From:<br>
                <select name="start">
                
            """)
        for town in towns:
            self.response.write("""<option>%s</option>"""%town)

        self.response.write("""</select> <br>""")
        self.response.write("""
                To:<br>
                <select name="end">
                
            """)
        for town in towns:
            self.response.write("""<option>%s</option>"""%town)  
        self.response.write("""</select> <br><br>""")
        self.response.write("""<input type='submit' method="post" value="Search route"> </input></form></div></body> """)      
        start=self.request.get("start")
        end=self.request.get("end")

       # self.response.write(data)
        if start!="" and end!="" :
            path=self.bfs(data,start,end)
            self.print_path(path)


app = webapp2.WSGIApplication([
    ('/MergeWord', MergeWord),('/Transfer',Transfer)
], debug=True)

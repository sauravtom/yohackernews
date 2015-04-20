#!/usr/bin/env python
from credentials import api_token
import webapp2,urllib,urllib2,json,jinja2,os,datetime
from google.appengine.ext import db


#contains links already yoyed
class AlreadyYoyed(db.Expando):
    url = db.StringProperty()

class Cron(webapp2.RequestHandler):
    def send_yo(self,link):
        data = {'api_token':api_token,'link':link}
        data = urllib.urlencode(data)
        request_object = urllib2.Request('http://api.justyo.co/yoall/', data)
        response = urllib2.urlopen(request_object)
        print response.read()

    def add_to_db(self,url):
        instance = AlreadyYoyed()
        instance.url =  url
        instance.put()

    def get(self):
        top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
        top_stories_json = json.loads(urllib2.urlopen(top_stories_url).read())
        
        for story_id in top_stories_json:
            print story_id
            story_url = "https://hacker-news.firebaseio.com/v0/item/%s.json?print=pretty"%story_id
            story_json = json.loads(urllib2.urlopen(story_url).read())

            already_yoyed = [instance.url for instance in AlreadyYoyed.all().fetch(1000000)]
            #print already_yoyed

            if story_json['type'] == 'story' and story_json['score'] >= 700 and story_json['url'] not in already_yoyed:
                #self.response.out.write(story_json)
                self.add_to_db(story_json['url'])
                self.send_yo(story_json['url'])
                return
    
    

application = webapp2.WSGIApplication([
    ('/cron', Cron)
    ],debug=True)
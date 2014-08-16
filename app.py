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
        hn_url = 'http://hnify.herokuapp.com/get/top'
        response = json.loads(urllib2.urlopen(hn_url).read())
        try:
            top = [i for i in response['stories'] if i['points'] > 500][0]
        except IndexError:
            return
        if top:
            print top['link']
            already_yoyed = [instance.url for instance in AlreadyYoyed.all().fetch(1000000)]
            print already_yoyed
            if top['link'] not in already_yoyed:
                self.add_to_db(top['link'])
                self.send_yo(top['link'])
            
application = webapp2.WSGIApplication([
    ('/cron', Cron)
    ],debug=True)
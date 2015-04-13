#!/usr/bin/env python
#Based on implementation from ltcs's "samplebot.py" source
#Uses twitter api and roomba api to tweet jokes and pictures!

import Queue
import random
import time
import os

from roomba.create2 import Create2
from foscam.foscam import camera_factory
from twython import Twython
from twython import TwythonStreamer

class RoombaStreamer(TwythonStreamer):
    def on_success(self, data):
        print "sanity on_suc"
        if 'roombie' in data:
            event_queue.put("roombie") 
        else:
            event_queue.put("joke")
 
    def on_error(self, status_code, data):
        print "sanity on_err"
        print status_code
        self.disconnect()

APP_KEY = 'AbX43tglwk1Uk3acmTc7rDrNk'
APP_SECRET = 'tHN3FwFssghYCCiOfzGUdTVpbfmowgDiva7sAiYVlQGxA5yaO1'
OAUTH_TOKEN = '3155143324-6mKrhLx2jAgjJ3ZcqYS00eBisLqEzCBsWU0QoRu'
OAUTH_TOKEN_SECRET = 'zP84bTrxcQKSmrYKHmpzzzsgQlcjmQ3U5DQxmaRpTOkx0'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

event_queue = Queue.Queue()



def sensor_callback(sensors):
    rand = random.randrange(4)
    if rand > 2:
        action = "joke"
    else:
        action = "snap"
    if sensors.bump_left or sensors.bump_right or not sensors.stasis:
        gap = time.time() - sensor_callback.last_event
        if gap > 5:
            sensor_callback.last_event = time.time()
            if not sensors.stasis:
                stuck_gap = time.time() - sensor_callback.stuck_time
                if stuck_gap > 3:
                    event_queue.put(action)
            elif sensors.bump_left and sensors.bump_right:
                event_queue.put(action)
            elif sensors.bump_left or sensors.bump_right:
                event_queue.put(action)


#Initialization

sensor_callback.last_event = 0 # Initialize static variable
sensor_callback.stuck_time = time.time()

camera = camera_factory()

roomba = Create2()
roomba.start()
roomba.sensor_stream((7,58), sensor_callback)
roomba.clean()

#Sets of responses for the roomba to say on Twitter

jokes = [   "Why did the Roomba cross the road? Roomba.clean()",
            "I have 1100011 problems and cleaning isn't one of them",
            "Like, Comment, and Subscribe!",
            "If I were a function, would you call() me?",
            "GET | www.xkcd.com:80",
            "I rarely see somebody I'm taller than",
            "Looking for: Shortest Path",
            "You're talking with a vaccum",
            "I'm clogging your Twitter because you forgot to clean me",
            "#robotsMasterRace",
            "Drop some food, I'm hungry",
            "Why did the Roomba cross the road? It had to dock",
            "I have 1100011 problems and EventWifi is one of them",
            "I'm $1000 worth of tweeting and cleaning",
            "iRobot, and now, I tweet too!",
            "I know we just met, but I had to bump into you"
            "I had a snarky comment, but I forgot it."
        ]

photo_tweets = [
    "#roombalife",           
    "#bumpyroad",
    "I'm so lost",
    "HellooooOOOOOooo",
    "Look at this picture I took",
    "I'm having so much fun at #bitcamp",
    "Ouch, someone just stepped on me",
    "Photography is not my forte",
    "#iamrobot",
    "Will you be my friend??",
    "How are you today??",
    "Looking good ;)",
    "follow4follow",
    "Dont step on meeeeee",
    "I just HAD to take this picture!",
    "Some things are better seen than cleaned",
    "I can take a picture for you. Just ask me to take a #roombie!",
    "Like, Comment, and Subscribe!",
    "This picture is very clean!",
    "Life is good",
    "Call out to @bitcmp!!"
    "#finalstretch"
    "Just Keep Cleaning, and Tweeting"
    "Sorry for all the ceiling pictures... People kept moving away"
]

#Initializing twitter stream so that we can scan for Roomba
streamer = RoombaStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

print "Sanity @try:"
try:
    while True:
        event = event_queue.get()
        streamer.statuses.filter(track = '@Bitcamp_Roomba')
        print "streamer sanity" 
        if event in ("snap", "stuck", "roombie"):
            #Stop the roomba to take a steady picture, resume
            roomba.safe()
            roomba.drive(0,0)
            time.sleep(1)  #reduce motion blur
            snap = camera.snapshot()
            path = "snaps/snap%d.jpg" % time.time()
            with open(path, "w") as outfile:
                outfile.write(snap)
            if event in "roombie":
                replyTo = streamer.user()
                tweet = "I took this picture for you, @" + replyTo 
            else:
                tweet = photo_tweets[random.randrange(len(photo_tweets))]
            photo = open(path, 'rb')
            twitter.update_status_with_media(status=tweet, media=photo)
            roomba.clean()
            
            #Adding sleep so that we don't spam Twitter too much
            time.sleep(10)
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError, e:
                    time.sleep(10)
                    os.remove(path)
        elif event in "joke":
            print "joke sanity"
            tweet = jokes[random.randrange(len(jokes))]
            twitter.update_status(status=tweet)
finally:
    roomba.safe()
    roomba.drive(0,0)   

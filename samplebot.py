#!/usr/bin/env python

import Queue
import random
import time

from roomba.create2 import Create2
from foscam.foscam import camera_factory

event_queue = Queue.Queue()

def sensor_callback(sensors):
    if sensors.bump_left or sensors.bump_right or not sensors.stasis:
        gap = time.time() - sensor_callback.last_event
        if gap > 5:
            sensor_callback.last_event = time.time()
            if not sensors.stasis:
                stuck_gap = time.time() - sensor_callback.stuck_time
                if stuck_gap > 3:
                    event_queue.put("stuck")
            elif sensors.bump_left and sensors.bump_right:
                event_queue.put("left|right")
            elif sensors.bump_left:
                event_queue.put("left")
            elif sensors.bump_right:
                event_queue.put("right")

sensor_callback.last_event = 0 # Initialize static variable
sensor_callback.stuck_time = time.time()


# Main program
print "sanity check"
camera = camera_factory()
print "sanity check 2"

r = Create2()
r.start()
print "sanity check 3"
r.sensor_stream((7,58), sensor_callback) 
r.clean()
print "sanity check 4"

sayings = ["Sorry about that", 
           "Excuse me", 
           "Pardon me",
           "On your left",
           "On your right",
           "Look out",
           "Make way for the bot!",
           "Coming through",
           "Whoops"]

try:
    print "sanity check 5"
    while True:
        print "sanity check 6"
        event = event_queue.get()
        if event in ("left", "right", "left|right", "stuck"):
            snap = camera.snapshot()
            path = "snaps/snap%d.jpg" % time.time()
            with open(path, "w") as outfile:
                outfile.write(snap)
            print "%s - %s: %s" % (event, sayings[random.randrange(len(sayings))], path)
finally:
    print "sanity check 7"
    r.safe()
    r.drive(0,0)

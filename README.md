# roomba_twitterbot
Raspberry Pi hack completed at Bitcamp 2015, a 36-hr hackathon hosted by the University of Maryland. 

twitterbot.py was the file authored exclusively by scmilburn and drakeling.
All other files were either from the roomba's parents: The Labroratory for Telecommunication Science, twython,
or various OS/apt-get installations.

To access the roomba's ethernet directly, you must connect to the 10.99.99.0/24 network.
roomba's pi: 10.99.99.1
roomba's webcam: 10.99.99.50

[EDIT: I just realized this networking configuration will be OS install dependant, this is how it was set up for us]

To run the twitterbot, simply type: twitter

Future iterations would include:
* Getting Twitter Streaming API to work so we can reply to tweets directed at the roomba to fulfill requests
  * to take a "roombie" - picture
  * to tell us a joke
  * go into "streaming" mode, feeding live video
  * drive in a straight line until collision, then resume clean mode
  * have the roomba follow others on twitter
  * to power down (would add a tweet on power up to save its alive, and another to declare it shutting down)
* Getting some form of object recognition through the webcam
  * have the webcam attempt to find certain objects before snapping a picture
  * have tweets request to find certain objects where the roomba currently is, and tweet about them
* Use of big data to procedurally write tweets
  * Use park data to have to rooma "Wish it was" at a random park
  * Give the roomba a sense of justice by saying it'll "Clean up" areas of higher crime
* Improving picture clean up (some pictures still made it through my delete calls)
* Improving crash behavior (right now, the cleaning routine will continue in some cases when the script dies)

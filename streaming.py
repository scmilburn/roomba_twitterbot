from twython import Twython

APP_KEY = 
APP_SECRET = 

twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentification_tokens()

OAUTH_TOKEN = auth['oath_token']

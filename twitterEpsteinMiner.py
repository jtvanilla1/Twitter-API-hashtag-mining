import twitter
from urllib.parse import unquote
from prettytable import PrettyTable
from collections import Counter
 
#API AUTHENTICATION VARIABLES---------------------------------------
CONSUMER_KEY = 'oDrAwJCwApR36whEvYaA1F4LF'
CONSUMER_SECRET = 'ExbTVWrz2ji9TNACeDwJKnfsuTIPopMEnNDrRxHfKJebLq7shs'
OAUTH_TOKEN = '1175128015296065536-hH4p3rcZlFrlBr7KE1y3IOq3CQOT8l'
OAUTH_TOKEN_SECRET = 'CHAQos4iEK0VVHUN4gYMfeX5LUwtbn12i5KjrnaO0JQco'
 
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                          CONSUMER_KEY, CONSUMER_SECRET)
 
twitter_api = twitter.Twitter(auth=auth)
 
#IDENTIFY TRENDING TOPIC POSTS------------------------------------
q = '#epsteinmurder'
count = 100
 
search_results = twitter_api.search.tweets(q=q, count=count)
statuses = search_results['statuses']
 
for _ in range(10):
   try:
       next_results = search_results['search_metadata']['next_results']
   except KeyError as e: # No more results when next_results doesn't exist
       break
      
   kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])
  
   search_results = twitter_api.search.tweets(**kwargs)
   statuses += search_results['statuses']
 
 
#TWEET ANATOMY----------------------------------------------------
status_texts = [ status['text']
                for status in statuses ]
 
screen_names = [ user_mention['screen_name']
                for status in statuses
                    for user_mention in status['entities']['user_mentions'] ]
 
hashtags = [ hashtag['text']
               for status in statuses
                   for hashtag in status['entities']['hashtags'] ]
 
locations = [ status['user']['location']
               for status in statuses]
 
words = [ w
         for t in status_texts
             for w in t.split() ]
 
#NORMALIZE LOCATIONS
transforms = [
 ('TEXAS', 'Texas, USA'),
 ('Texas', 'Texas, USA'),
  ('Southern Florida', 'Florida, USA'),
 ('South Florida', 'Florida, USA'),
  ('Middle Georgia', 'Georgia, USA'),
  ('MI', 'Michigan, USA'),
  ('phoenix', 'Phoenix, AZ'),
 ('Hollywood, Los Angeles', 'Los Angeles, CA'),
 ('Anywhere USA', 'USA'),
 ('AnywhereUSA', 'USA'),
 ('Ohio', 'Ohio, USA'),
 ('United States of America', 'USA'),
 ('United States', 'USA'),
 ('USA ', 'USA')]
 
for i, _ in enumerate(locations):
   for transform in transforms:
       locations[i] = locations[i].replace(*transform)
 
#DISPLAY TABLE OF DATA--------------------------------------------
with open('output.txt','a') as myfile:
for label, data in (('Word', words),
                    ('Screen Name', screen_names),
                    ('Hashtag', hashtags),
                    ('Location', locations)):
    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    [ pt.add_row(kv) for kv in c.most_common()[:30] ] #top 30 results
    pt.align[label], pt.align['Count'] = 'l', 'r'
    print(pt)
    table_txt = pt.get_string()
    myfile.write(table_txt)
    myfile.write('\n')
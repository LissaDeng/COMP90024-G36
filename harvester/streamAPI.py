import tweepy
import json
import couchdb
import threading
import sentiment
from sentiment import sentiment_analyse_angry
from sentiment import sentiment_analyse_gluttony

class MyStreamListener(tweepy.StreamListener):

    tweet_number=0   # Count the tweets number

    def __init__(self, couchdb, harvester_id, max_tweets):
        self.harvester_id = harvester_id
        self.couchdb = couchdb
        self.max_tweets=max_tweets # max number of tweets to get

    def on_data(self, data):
        self.tweet_number += 1
        #print(self.tweet_number) 
        
        dict_data = json.loads(data)
        
        point = []
        if dict_data['geo'] and 'coordinates'in dict_data['geo'] and dict_data['geo']['coordinates']:
            point_type = 'poi'
            point = dict_data['geo']['coordinates']
        elif dict_data['coordinates'] and 'coordinates'in dict_data['coordinates'] \
        and dict_data['coordinates']['coordinates']:
            point_type = 'poi'
            point = [dict_data['coordinates']['coordinates'][1],dict_data['coordinates']['coordinates'][0]]
        elif dict_data['place'] and 'bounding_box' in dict_data['place'] and \
        isinstance(dict_data['place']['bounding_box'], dict) and 'coordinates' in dict_data['place']['bounding_box']\
        and dict_data['place']['bounding_box']['coordinates']:
            point_type = dict_data['place']['place_type']
            coordinates = dict_data['place']['bounding_box']['coordinates'][0]
            lat = (coordinates[0][1] + coordinates[1][1])/2
            lng = (coordinates[0][0] + coordinates[2][0])/2
            point = [lat,lng]
        else:
            point = None
            point_type = None
            #print(point)
                
        if not point is None:

            # Get the attached picture url first
            url = None
            if 'entities' in dict_data and isinstance(dict_data['entities'], dict):
                    if 'media' in dict_data['entities']:
                        media1 = dict_data['entities']['media'][0]
                        if 'media_url' in media1:
                            url = media1['media_url']
                   
            if 'retweeted_status' in dict_data and isinstance(dict_data['retweeted_status'], dict):
                    if 'extended_tweet' in dict_data['retweeted_status'] \
                    and isinstance(dict_data['retweeted_status']['extended_tweet'], dict):
                            if 'entities' in dict_data['retweeted_status']['extended_tweet'] \
                            and isinstance(dict_data['retweeted_status']['extended_tweet']['entities'], dict):
                                if 'media' in dict_data['retweeted_status']['extended_tweet']['entities']:
                                    media2 = dict_data['retweeted_status']['extended_tweet']['entities']['media'][0]
                                    if 'media_url' in media2:
                                        url = media2['media_url']

                            elif 'extended_entities' in dict_data['retweeted_status']['extended_tweet'] \
                            and isinstance(dict_data['retweeted_status']['extended_tweet']['extended_entities'], dict):
                                if 'media' in dict_data['retweeted_status']['extended_tweet']['entities']:
                                    media3 = dict_data['retweeted_status']['extended_tweet']['entities']['media'][0]
                                    if 'media_url' in media3:
                                        url = media3['media_url']

            # Sentiment analysis starts
            # Recognize whether the current tweet belongs to 'angry'
            angry_analysis = sentiment_analyse_angry(dict_data['text'])
            # Recognize whether the current tweet belongs to 'gluttony'
            gluttony_analysis = sentiment_analyse_gluttony(dict_data['text'], url)
            sentiment = {"angry_analysis": angry_analysis, "gluttony_analysis": gluttony_analysis}

            # Load raw data into a dictionary and filter the infomation we need
            # Only load the data from the time period we need
            filter_data = {'_id':dict_data['id_str'],'created_at':dict_data['created_at'],\
                                'text':dict_data['text'],'user':dict_data['user'],'geo':dict_data['geo'],\
                                'coordinates':dict_data['coordinates'],'place':dict_data['place'],\
                                'image': url, 'sentiment':sentiment,'point':point,'point_type':point_type,'point_name':dict_data['place']['name']}
            
            # Store data in couchdb
            if filter_data['_id'] not in self.couchdb:
                self.couchdb.save(filter_data)

        # if the tweet number more than max num, stop the api
        if self.tweet_number >= self.max_tweets:
            print('Limit of '+ str(self.max_tweets) + ' tweets reached.')
            return False # Stop the harvester
        
        return True # Continue the harvester
    
    def on_error(self, status_code):
        if status_code == 420:
            print("Reached the limit rate") 
            return False
        print(status)
        return True

class StreamAPI(threading.Thread):
    def __init__(self, api, stream_loc, harvester_id, couchdb, maxTweets):
        threading.Thread.__init__(self)
        self.api = api
        self.stream_loc = stream_loc
        self.harvester_id = harvester_id
        self.couchdb = couchdb
        self.maxTweets = maxTweets # Input the max number of tweets

        if not self.api:
            print("No API Authentication in stream")

    def run(self):
        myStreamListener = MyStreamListener(self.couchdb, self.harvester_id, self.maxTweets)
        myStream = tweepy.Stream(auth = self.api.auth, listener=myStreamListener)
        myStream.filter(locations = self.stream_loc) 

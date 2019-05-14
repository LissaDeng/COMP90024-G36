import tweepy
import json
import couchdb
import threading
import sentiment
from sentiment import sentiment_analyse_angry
from sentiment import sentiment_analyse_gluttony

class SearchAPI(threading.Thread):
    def __init__(self, api, search_loc, harvester_id, couchdb, sinceId, maxTweets):
        threading.Thread.__init__(self)
        self.api = api
        self.search_loc = search_loc
        self.harvester_id = harvester_id
        self.couchdb = couchdb
        self.sinceId = sinceId
        self.maxTweets = maxTweets # Input the max number of tweets

        if not self.api:
            print("No API Authentication in search")

    def run(self):

        tweetsPerQry = 100  # this is the max the API permits
        max_id = -1

        tweetCount = 0
        #print("Downloading max {0} tweets".format(maxTweets))

        places = self.api.geo_search(query=self.search_loc, granularity="city")
        place_id = places[0].id
        searchQuery = "place:%s" % place_id  # this is the place info for searching

        while tweetCount < self.maxTweets:
                try:
                        if (max_id <= 0):
                            if (not self.sinceId):
                                new_tweets = self.api.search(q = searchQuery, count = tweetsPerQry)
                            else:
                                new_tweets = self.api.search(q = searchQuery, count = tweetsPerQry, since_id = self.sinceId)
                        else:
                            if (not self.sinceId):
                                new_tweets = self.api.search(q = searchQuery, count = tweetsPerQry, max_id = str(max_id - 1))
                            else:
                                new_tweets = self.api.search(q = searchQuery, count = tweetsPerQry, max_id = str(max_id - 1), since_id = self.sinceId)
                                        
                        if not new_tweets:
                            print("No more tweets found")
                            break
                                
                        for tweet in new_tweets:
                            # Load raw data into a dictionary and filter the infomation we need
                            # Only load the data from the time period we need
                            point = []
                            if tweet._json['geo'] and 'coordinates'in tweet._json['geo'] and tweet._json['geo']['coordinates']:
                                point_type = 'poi'
                                point = tweet._json['geo']['coordinates']
                            elif tweet._json['coordinates'] and 'coordinates'in tweet._json['coordinates'] \
                            and tweet._json['coordinates']['coordinates']:
                                point_type = 'poi'
                                point = [tweet._json['coordinates']['coordinates'][1],tweet._json['coordinates']['coordinates'][0]]
                            elif tweet._json['place'] and 'bounding_box' in tweet._json['place'] and \
                            isinstance(tweet._json['place']['bounding_box'], dict) and 'coordinates' in tweet._json['place']['bounding_box']\
                            and tweet._json['place']['bounding_box']['coordinates']:
                                point_type = tweet._json['place']['place_type']
                                coordinates = tweet._json['place']['bounding_box']['coordinates'][0]
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
                                if 'entities' in tweet._json and isinstance(tweet._json['entities'], dict):
                                        if 'media' in tweet._json['entities']:
                                            media1 = tweet._json['entities']['media'][0]
                                            if 'media_url' in media1:
                                                url = media1['media_url']
                                       
                                if 'retweeted_status' in tweet._json and isinstance(tweet._json['retweeted_status'], dict):
                                        if 'extended_tweet' in tweet._json['retweeted_status'] \
                                        and isinstance(tweet._json['retweeted_status']['extended_tweet'], dict):
                                                if 'entities' in tweet._json['retweeted_status']['extended_tweet'] \
                                                and isinstance(tweet._json['retweeted_status']['extended_tweet']['entities'], dict):
                                                    if 'media' in tweet._json['retweeted_status']['extended_tweet']['entities']:
                                                        media2 = tweet._json['retweeted_status']['extended_tweet']['entities']['media'][0]
                                                        if 'media_url' in media2:
                                                            url = media2['media_url']

                                                elif 'extended_entities' in tweet._json['retweeted_status']['extended_tweet'] \
                                                and isinstance(tweet._json['retweeted_status']['extended_tweet']['extended_entities'], dict):
                                                    if 'media' in tweet._json['retweeted_status']['extended_tweet']['entities']:
                                                        media3 = tweet._json['retweeted_status']['extended_tweet']['entities']['media'][0]
                                                        if 'media_url' in media3:
                                                            url = media3['media_url']

                                # Sentiment analysis starts
                                # Recognize whether the current tweet belongs to 'angry'
                                angry_analysis = sentiment_analyse_angry(tweet._json['text'])
                                # Recognize whether the current tweet belongs to 'gluttony'
                                gluttony_analysis = sentiment_analyse_gluttony(tweet._json['text'], url)
                                sentiment = {"angry_analysis": angry_analysis, "gluttony_analysis": gluttony_analysis}
                                
                                # Get other fields 
                                filter_data = {'_id':tweet._json['id_str'],'created_at':tweet._json['created_at'],\
                                                'text':tweet._json['text'],'user':tweet._json['user'],'geo':tweet._json['geo'],\
                                                'coordinates':tweet._json['coordinates'],'place':tweet._json['place'],\
                                                'image':url, 'sentiment':sentiment,'point':point,'point_type':point_type,'point_name':self.search_loc}

                                # Store data in couchdb
                                if filter_data['_id'] not in self.couchdb:
                                    self.couchdb.save(filter_data)
                                    
                        tweetCount += len(new_tweets)
                        max_id = new_tweets[-1].id
                            
                except tweepy.TweepError as e:
                        # pass if any error
                        print("some error : " + str(e))
                        continue




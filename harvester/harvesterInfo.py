import tweepy
import couchdb

class HarvesterInfo:
    def __init__(self):
        #self.couchdb_username = 'g36'
        #self.couchdb_password = '1q2w3e'
        #self.couchdb_address = 'localhost:5984/'
        #self.couchdb_database = 'tweets'
        #self.couchdb_server = couchdb.Server('http://g36:1q2w3e@localhost:5984/')

        self.api = [0,1,2,3,4,5]
        self.search_loc_str = [0,1,2,3,4,5]
        self.stream_loc = [0,1,2,3,4,5]

        # 1-Lissa-1
        self.api[0] = self.load_api(api_address)
        self.search_loc_str[0] = "Melbourne"
        self.stream_loc[0] = [143.5,-39,146,-37]

        # 2-Shuohang-1
        self.api[1] = self.load_api(api_address)
        self.search_loc_str[1] = "Sydney"
        self.stream_loc[1] = [149.5,-34.6,152,-32.3]

        # 3-Patrick-1
        self.api[2] = self.load_api(api_address)
        self.search_loc_str[2] = "Brisbane"
        self.stream_loc[2] = [152,-27.5,154,-26]

        # 4-Shuohang-2
        self.api[3] = self.load_api(api_address)
        self.search_loc_str[3] = "Gold Coast"
        self.stream_loc[3] = [152,-29,154,-27.5]

        # 5-Aaron-1
        self.api[4] = self.load_api(api_address)
        self.search_loc_str[4] = "Perth"
        self.stream_loc[4] = [115,-32.8,116.8,-31.5]

        # 6-LGN-1
        self.api[5] = self.load_api(api_address)
        self.search_loc_str[5] = "Adelaide"
        self.stream_loc[5] = [138.2,-35.5,139,-34.3]
        

    def load_api(self,consumer_key, consumer_key_secret,consumer_token, consumer_token_secret):
        ''' Function that loads the twitter API after authorizing the user. '''
        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        auth.set_access_token(consumer_token, consumer_token_secret)
        # load the twitter API via tweepy
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if api:
            return api
        else:
            return None

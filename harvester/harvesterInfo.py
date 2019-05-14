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
        self.api[0] = self.load_api('A6gbF6A6pxRNraGtl9wrkmz47','vgrwuG5EWgH71amBuq9Rcc1sXmuoCKWaNqjiYoBKCutayW9MiN',\
                            '1120979677282099200-fjGnDluikFvo2p7nGmmnBCmxKpL3bI','qrQt6A45oeR1WTcpG0VExaGgHXRxQnF7hGImJrS0SVVAA')
        self.search_loc_str[0] = "Melbourne"
        self.stream_loc[0] = [143.5,-39,146,-37]

        # 2-Shuohang-1
        self.api[1] = self.load_api('pCTI70auSvjGiCEyT8HCN1IvR','49tmGUKs41OVur49kGJaLgnK57tj457agi3MSWpwV5bTGg6bKx',\
                            '971617279317127168-TvNe1uZ7G5dybvt3xlpMOdBaUUdC4Az','gktuQROh9TLIg9t5X2HxYN5sQ23WZeUT7iLuHMiUCBHuH')
        self.search_loc_str[1] = "Sydney"
        self.stream_loc[1] = [149.5,-34.6,152,-32.3]

        # 3-Patrick-1
        self.api[2] = self.load_api('UM4DbYgS6wBRsqcrkJVlZNEUA','v5vxMdCxhEdYELovMTunZ33vWAxX7NTpUMF2ikVZWgjR6T0SHn',\
                            '1123418386023583744-nDKfsZiTUUaP38L6KgziJG5nnoGM4j','jYuFVRVOr18t1HEF92MSv3Ws4dPeX562Rmo0nYk1oZOA2')
        self.search_loc_str[2] = "Brisbane"
        self.stream_loc[2] = [152,-27.5,154,-26]

        # 4-Shuohang-2
        self.api[3] = self.load_api('eJ9km3J0kYXETiTz9PZhpExvt','jTnZ1B2lr3xpsYJFzHe19kMo1Ky7wOtXg9mqCgpjPcj4O9L020',\
                            '1123399526465687552-bJSOyinJsqUXQGcK2C09gwRlI0LG9i','ilMNccZ3WuosQv6rB05Cj4zxxIWjeAH8GX7ZZruED5QUx')
        self.search_loc_str[3] = "Gold Coast"
        self.stream_loc[3] = [152,-29,154,-27.5]

        # 5-Aaron-1
        self.api[4] = self.load_api('M0j1UBifTBXXElvpgoE9YS7oU','x73NzHS4UdjklZcVWJGNMv4EZAWrGbJoBTVPEyuaTyjKJQCDx8',\
                            '1122001971961950208-rQiqaTvqBlu8JfnfKuPx2bxfW6K9Bd','Znd2oh69j6jPRCKMcQL79VrVLRW9TO4bE4naE5LoaU9pn')
        self.search_loc_str[4] = "Perth"
        self.stream_loc[4] = [115,-32.8,116.8,-31.5]

        # 6-LGN-1
        self.api[5] = self.load_api('dMXtWDGEnB8dXrHhwyGUEMctO','4qFc8IfUT9NrYgI4uyaUYWqoqPoCYU0u3c9lySOv04P203Ry8m',\
                            '1123196162566017025-ugvh7iPoDoWX587dYg6WYqxdvH6CW3','WHnOO86CrkWFsv2jzkkIPpSWmZJncfu70q7H1L2dO1luf')
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

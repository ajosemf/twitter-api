import re, os
import pandas as pd
from unicodedata import normalize
from src.apis.twitter import TwitterAPI


class TwitterMonitor(object):
    
    def __init__(self):
        self._twitter_api = TwitterAPI()
        self._status_processor = TwitterStatusProcessor()
        self._search_tags = (os.getenv('SEARCH_TAGS')).split(',')
        self._name_social_network = 'twitter'
        self._screen_names = ['Record News', 'GloboNews']
        print("Twitter Monitor initialized")
    
        
    def run(self):
        self._get_data()
        
    
    def _get_data(self):
        tags = set(map(str.lower, map(self._normalize_text, self._search_tags)))
        regex_string = '|'.join(tags)
        pattern = re.compile(regex_string)
        data = list()
        
        for screen_name in self._screen_names:
            print('Fetching data from {}'.format(screen_name))
            data += self._fetch_data(screen_name, pattern, limit=50)
                            
        if data:
            print(f'{len(data)} posts collected from media')
            df = pd.DataFrame(data)
            print(df.head())
            print(df.tail())
        
        
    def _fetch_data(self, screen_name, pattern, limit=0, datetime_limit=None):
        """Fetch tweets from account timeline and store in file

        Args:
            screen_name (str): Screen name of the social network account
            pattern (re.pattern): Pattern object from re module
            limit (int, optional): Num of posts to be fetched. \
                If 0 passed, will be fetched 20 posts. Defaults to 0.
            datetime_limit (datetime, optional): Datetime limit of posts datetime publication. Defaults to None.

        Returns:
            list: List of dicts, each dict representing one tweet
        """
        
        try:
            tweets = list()
            self._status_processor.account_screen_name = screen_name
            
            for status in self._twitter_api.fetch_timeline(screen_name=screen_name, limit=limit):
                tweet = self._status_processor.process(status)
                text_post = self._normalize_text(tweet['text_post']).lower()
                if datetime_limit and tweet['datetime_post'] <= datetime_limit:
                    break
                if pattern.search(text_post):
                    tweets.append(tweet)
            return tweets
        except:
            print('An exception occurred when trying to collect twitter statuses from {}'.format(screen_name))
            raise
    
    
    def _normalize_text(self, text):
        return normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')


class TwitterStatusProcessor(object):
    
    def __init__(self):
        self.account_screen_name = None
        
        
    def process(self, status):
        tweet = dict()
        tweet['text_post'] = ''
        tweet['num_likes'] = 0
        tweet['num_shares'] = 0
        tweet['id_post_social_media'] = status.id
        
        if hasattr(status, "retweeted_status"):  # if is a retweet
            
            tweet['parent_id_post_social_media'] = status.retweeted_status.id
            
            try:
                tweet['text_post'] = status.retweeted_status.extended_tweet["full_text"]
            
            except AttributeError:    
                try:
                    tweet['text_post'] = status.retweeted_status.full_text
                except AttributeError:
                    tweet['text_post'] = status.retweeted_status.text
            
            finally:
                tweet['num_likes'] = status.retweeted_status.favorite_count
                tweet['num_shares'] = status.retweeted_status.retweet_count
        
        else:
            tweet['parent_id_post_social_media'] = None
            
            try:
                tweet['text_post'] = status.extended_tweet["full_text"]
            
            except AttributeError:
                try:
                    tweet['text_post'] = status.full_text
                except AttributeError:
                    tweet['text_post'] = status.text
        
        tweet['text_post'] = tweet['text_post'].replace("\n", " ")
        tweet['datetime_post'] = status.created_at
        
        tweet['account_screen_name'] = self.account_screen_name
        tweet['num_likes'] = status.favorite_count or tweet['num_likes']
        tweet['num_shares'] = status.retweet_count or tweet['num_shares']
        return tweet

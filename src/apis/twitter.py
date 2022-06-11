import os
import tweepy
    
    
class TwitterAPI(object):
    
    def __init__(self):
        self._api = None
        self._connect()
        print("Twitter API initialized")

        
    def _connect(self):
        if not self._api:
            try:
                auth = tweepy.OAuthHandler(
                    os.getenv('CONSUMER_KEY'),
                    os.getenv('CONSUMER_SECRET'),
                    os.getenv('ACCESS_TOKEN'),
                    os.getenv('ACCESS_TOKEN_SECRET')
                )
                self._api = tweepy.API(auth)
            except:
                print('Unable to connect to Twitter API.')
                raise
            
    
    def fetch_timeline(self, screen_name=None, mode='items', limit=0):
        """Returns the most recent statuses posted from the \
            authenticating user or the screen_name user specified.

        Args:
            screen_name (str, optional): screen name of the user. Defaults to None.
            mode (str, optional): possible values {'items', 'pages'}. Defaults to 'items'.
            limit (int, optional): num of items or pages. Value 0 returns the 20 most recent. Defaults to 0.

        Returns:
            tweepy.Cursor: Tweepy Cursor object
        """
        
        try:
            cursor = tweepy.Cursor(self._api.user_timeline,
                                id=screen_name,
                                tweet_mode='extended')
            if mode == 'items':
                return cursor.items(limit)
            if mode == 'pages':
                return cursor.pages(limit)
        except:
            raise

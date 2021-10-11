import tweepy
import os
from pathlib import Path
from dotenv import load_dotenv
import time
import logging
import webbrowser
import pandas as pd


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

api_key = os.environ.get('APP_API_KEY')
api_key_secret = os.environ.get("APP_SECRET_KEY")
access_token = os.environ.get("APP_ACCESS_TOKEN")
access_token_secret = os.environ.get("APP_ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get('APP_BEARER_TOKEN')

callback_uri = 'oob'

# OAuthHandler instance
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Authenticate the app and send the user to the url
# redirect_url = auth.get_authorization_url()

# Get access token through the browser
# webbrowser.open(redirect_url)
# user_pin_input = input('Please enter your pin! ')
# auth.get_access_token(user_pin_input)
# auth.set_access_token(auth.access_token, auth.access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
current_user = os.environ.get("TWITTER_NAME")

# test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")



class Likes:
    def __init__(self, username):
        self.username = username
        

    # Update status 
    def update_status(self):   
        api.update_status('This is a test tweet')


    # Get user by id
    def get_user(self, screen_name):
        user = api.get_user(screen_name=screen_name)
        user = user.id
        return user


    # Get user details by user id
    def get_user_details(self, user_id):
        user = api.get_user(screen_name=user_id)
        print(f'User: {user.screen_name}')
        print(f'Followers Count: {user.followers_count}')
        print(f'Created On: {user.created_at}')
        print(f'URL: {user.expanded_url}')


    # Follow by username
    def follow_user(self, screen_name):
        api.create_friendship(screen_name=screen_name)


    # Get a users timeline object
    def get_user_timeline(self, screen_name):
        user = api.get_user(screen_name=screen_name)
        user_timeline = user.timeline()
        return user_timeline


    # Follow account followers (items_count is the number of followers you wish to follow)
    def accountFollowers(self, screen_name, item_count):
        for i, _id in enumerate(tweepy.Cursor(api.get_friend_ids, screen_name=screen_name).items(item_count)):
            print('Rinning...')
            if i % 250 == 0 and i > 0:
                print(i)
                print('Sleeping for 15 minutes')
                time.sleep(900)
            try:
                api.create_friendship(user_id=_id)
                print(f'Following: {_id}')
            except Exception as e:
                print(e)
        

    # Unfollow all
    def unfollowAll(self):
        for screen_name in tweepy.Cursor(api.get_friends, screen_name=current_user).items():
            api.destrop_friendship(username)


    # Write your timeline info to a csv file
    def write_home_timeline_to_csv(self):
        columns = set()
        allowed_types = [str, int]
        tweets_data = []
        my_timeline = api.home_timeline()

        for tweet in my_timeline:
            tweet_dict = dict(vars(tweet))
            keys = tweet_dict.keys()
            single_tweet_data = {'user': tweet.user.screen_name, 'author': tweet.author.screen_name}
            for k in keys:
                try:
                    v_type = type(tweet_dict[k])
                except:
                    v_type = None
                if v_type != None:
                    if v_type in allowed_types:
                        single_tweet_data[k] = tweet_dict[k]
                        columns.add(k)
            tweets_data.append(single_tweet_data)

        header_cols = list(columns)
        header_cols.append('user')
        header_cols.append('author')

        df = pd.DataFrame(tweets_data, columns=header_cols)
        df.to_csv('tweets.csv', sep=',')
    

    # Write a users timeline info to a csv file
    def write_timeline_to_csv(self, timeline):
        columns = set()
        allowed_types = [str, int]
        tweets_data = []

        for tweet in timeline:
            tweet_dict = dict(vars(tweet))
            keys = tweet_dict.keys()
            single_tweet_data = {'user': tweet.user.screen_name, 'author': tweet.author.screen_name}
            for k in keys:
                try:
                    v_type = type(tweet_dict[k])
                except:
                    v_type = None
                if v_type != None:
                    if v_type in allowed_types:
                        single_tweet_data[k] = tweet_dict[k]
                        columns.add(k)
            tweets_data.append(single_tweet_data)

        header_cols = list(columns)
        header_cols.append('user')
        header_cols.append('author')

        df = pd.DataFrame(tweets_data, columns=header_cols)
        df.to_csv('tweets.csv', sep=',')


    # Like all tweets on a users timeline
    def likePosts(self, screen_name, item_count):
        for i, status in enumerate(tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items(item_count)):
            print('Rinning...')
            if not status.favorited and i % 250 == 0 and i > 0:
                print(i)
                print('Sleeping for 15 minutes')
                time.sleep(900)

            if status.author.screen_name != current_user:
                if not status.favorited:
                    try:
                        api.create_favorite(status.id)
                        print(f'Liked: {status.id}')
                    except Exception as e:
                        print(e)


    # Get a tweets status objects (This can be used to retweet or reply)
    def get_status_object(self, screen_name):
        user_timeline = screen_name.timeline()
        user_timeline_status_obj = user_timeline[0]
        status_obj_id = user_timeline[0].id
        status_obj_screen_name = status_obj_id.user.screen_name
        status_obj_url = f'https://twitter.com/{status_obj_screen_name}/status/{status_obj_id}'


    # Retweet
    def retweet(status_obj_id):
        api.retweet(status_obj_id)



pp = Likes(current_user)

# This function follows all the followers of a given account (Add the account and number of followers to follow)
pp.accountFollowers('raritytools', 500)

# This function likes all the posts on a given accounts timeline (Add the account and number of posts to like)
pp.likePosts('raritytools', 500)

import os, re
import pandas as pd
from config import Hyper
from user_location import UserLocation
from helper import Helper
from sentiment import Sentiment
from database import Data

'''
    This program is the second in a suite of programs to be executed in this order
    1/ App - gets tweets from Twitter API
    2/ Location - gets the country of the tweet from user location
    3/ Annotate - calculates the sentiment of each tweet
    4/ Wordcload - shows the words most in use in tweets from different countries
    5/ Datapreparation - gets the data in the correct form
    6/ Transformer - builds a transformer model from the tweets
'''
def main():
    Helper.printline("** Location Started\n")
    Helper.printline("     ** Started: Calculate country from User Location")
    d = Data()
    u = UserLocation(d)
    d.get_tweet_user_locations()
    tweets = d.tweet_user_locations
    tweet_cnt = 0
    Helper.printline("Start reading tweets")
    for tweet in tweets:
        tweet_cnt += 1
        if tweet_cnt % 50000 == 0:
            Helper.printline(f"{tweet_cnt} tweets processed")
        tweet_id, user_location = tweet    
        is_valid = u.validate_user_location(user_location)
        if is_valid == False:
            continue
        
        country_code = u.locator(user_location) 
     
        if len(country_code) == 2:
            d.save_tweet_country_code(tweet_id, country_code)
    
    Helper.printline(f"loctaion from dictionary: {u.from_dict_cnt}, from geopy: {u.from_geopy_cnt}")        
    Helper.printline(f"All {tweet_cnt} tweets processed")        
    Helper.printline("\n** Location Ended")

def get_values(tweet):
    for key in tweet.keys():
        user_location = key
        
    tweet_id = tweet[user_location]
    return user_location,tweet_id
        

if __name__ == "__main__":
    main()
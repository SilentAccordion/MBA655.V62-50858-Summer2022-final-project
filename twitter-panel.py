from tkinter import Tk, Label, Button
# import datetime
import tweepy

from API_keys import bearer_token


class TwitterPanelGUI:
    def __init__(self, master):
        self.master = master
        master.title("Twitter Panel GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Tweet", 
                                   command=self.get_tweet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

    def get_tweet(self):

        # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # auth.set_access_token(access_token, access_token_secret)

        # You can provide the consumer key and secret with the access token and access
        # token secret to authenticate as a user
        client = tweepy.Client(bearer_token=bearer_token)

        # Setup fileCache to avoid issues with API Limits
        # cache_dir = "./cache/"
        # timeout = 60

        # cache = client.FileCache(cache_dir, timeout)

        response = client.search_recent_tweets("Tweepy")
        
        # The method returns a Response object, a named tuple with data, includes,
        # errors, and meta fields
        print(response.meta)

        # In this case, the data field of the Response returned is a list of Tweet
        # objects
        tweets = response.data

        # Each Tweet object has default ID and text fields
        for tweet in tweets:
            print(tweet.id)
            print(tweet.text)

        # By default, this endpoint/method returns 10 results
        # You can retrieve up to 100 Tweets by specifying max_results
        response = client.search_recent_tweets("Tweepy", max_results=100)


root = Tk()
my_gui = TwitterPanelGUI(root)
root.mainloop()

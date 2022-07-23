from tkinter import Tk, Label, Button
# import datetime
import tweepy

from API_keys import consumer_key, consumer_secret,\
                     access_token, access_token_secret


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

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Setup fileCache to avoid issues with API Limits
        cache_dir = "./cache/"
        timeout = 60

        cache = tweepy.FileCache(cache_dir,timeout)

        # Initialize the API
        api = tweepy.API(auth_handler=auth, cache=cache)

        ## Print out current rate limits status
        # print(api.rate_limit_status())

        q = "@realDonaldTrump AND -filter:retweets AND -filter:replies"

        search_tweets = tweepy.Cursor(api.search,
                            tweet_mode = 'extended',
                            q = q,
                            lang = 'en').items(100)


root = Tk()
my_gui = TwitterPanelGUI(root)
root.mainloop()

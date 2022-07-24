from tkinter import Tk, Label, Button, Text,\
                    INSERT, END, Canvas, Frame

from tkinter.messagebox import showerror, showwarning, showinfo

# import datetime
import random

import tweepy

# Image Libraries
from io import BytesIO
# import base64
# from urllib.request import urlopen
from PIL import Image, ImageTk, UnidentifiedImageError
import requests


# Local variables
from API_keys import consumer_key, consumer_secret,\
                     access_token, access_token_secret                     


class TwitterPanelGUI:
    def __init__(self, master):
        self.master = master
        master.title("Twitter Box")

        self.label = Label(master, text="Find Random Montana Tweets")
        self.label.pack()

        self.button_frame = Frame(master)

        self.tweet_button = Button(self.button_frame, text="Next Tweet", 
                                   command=self.get_tweet)
        self.tweet_button.pack(side="right")

        self.close_button = Button(self.button_frame, 
                                   text="Close Twitter Box",
                                   command=self.master.quit)
        self.close_button.pack(side="right")

        self.button_frame.pack()

        self.tweet_user = Label(self.master, text="")
        self.tweet_user.pack()

        self.tweet_frame = Frame(master)

        # create a white canvas
        self.cv = Canvas(self.tweet_frame, bg='white', width=48, height=48)
        # side='top', fill='both', expand='yes'
        self.cv.pack(side="left", fill=None, expand=False)

        # Create text widget and specify size.
        self.tweet = Text(self.tweet_frame, height=6, width=100)
        self.tweet.pack(side="right", fill=None, expand=True)

        self.tweet_frame.pack()

    def greet(self):
        print("Greetings!")

    def get_tweet(self):

        if '' == consumer_key:
            showerror(title="Error", message="Invalid Consumer Key")
            return

        if '' == consumer_secret:
            showerror(title="Error", message="Invalid Consumer Secret")
            return
        
        if '' == access_token:
            showerror(title="Error", message="Invalid Access Token")
            return
        
        if '' == access_token_secret:
            showerror(title="Error", message="Invalid Token Secret")
            return
        
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret,
            access_token, access_token_secret
        )

        api = tweepy.API(auth)

        # If the authentication was successful, this should print the
        # screen name / username of the account
        # print(api.verify_credentials().screen_name)

        tweets = api.search_tweets(q='Montana', lang='en')

        # Check length of tweet array
        # print(len(tweets))

        if 0 == len(tweets):
            showwarning(title="Alert", message="No Tweets have been found \
                                                that match the search term")
            return

        # Display all tweets
        # print(tweets)

        # Shuffle tweets to get a fresh one everytime
        random.shuffle(tweets)

        tweet = tweets[0]

        # Print details from API for tweet
        # print(tweet)

        # Print status from single tweet
        # print(tweet.text)

        dirty_tweet = tweet.text

        # https://stackoverflow.com/a/46173665
        char_list = [dirty_tweet[j]
                     for j in range(len(dirty_tweet))
                     if ord(dirty_tweet[j]) in range(65536)]
        
        clean_tweet = ''

        # Rebuild tweet with allows Charaters
        for j in char_list:
            clean_tweet = clean_tweet+j

        if len(clean_tweet) < len(dirty_tweet):
            showwarning(title="Alert", message="Tweet has been has been \
                                                modified from its original \
                                                version. It has been formatted\
                                                to fit this screen.")

        # Insert The Tweet.
        self.tweet.delete(1.0, END)

        message = clean_tweet

        # ' at ' + tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S")

        self.tweet.insert(INSERT, message)

        self.tweet_user.config(text='@' + tweet.user.screen_name)

        # https://www.daniweb.com/programming/software-development/code/440946/display-an-image-from-a-url-tkinter-python

        # Test with local file
        # image = Image.open('./avatar.jpeg')

        image_url = tweet.user.profile_image_url

        # a little more than width and height of image
        # w = 48
        # h = 48
        # x = 0
        # y = 0
        # use width x height + x_offset + y_offset (no spaces!)
        # root.geometry("%dx%d+%d+%d" % (w, h, x, y))

        # print(image_url)
        # Doesn't support jpg
        # image_byt = urlopen(image_url).read()
        # image_b64 = base64.encodebytes(image_byt)
        # print(image_b64)

        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            showinfo(title="Alert", message="Tweet Avatar failed\
                                                to load")
            return

        photo = ImageTk.PhotoImage(image)

        # put the image on the canvas with
        # create_image(xpos, ypos, image, anchor)
        self.cv.create_image(0, 0, image=photo, anchor='nw')
        
        # Force a refresh to see image
        self.master.mainloop()


root = Tk()
my_gui = TwitterPanelGUI(root)
root.mainloop()

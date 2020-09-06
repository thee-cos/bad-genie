###### Bad Genie Twitter Bot ######
# Created by Evan
# 28.7.2020
# Last updated
# 6.9.2020

from matplotlib import pyplot as plt
import numpy as np
import tweepy
import random
import datetime
import time

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def check_tweet_code(text, needed_string):
    text_lower = text.lower()
    # Guess I can just use python .find() method but I'll keep this because I can
    # returns text after check string until punctuation
    # part 1: check for string
    len_needed_string = len(needed_string)
    found_loc = text_lower.find(needed_string)
    # Part 2: When found, find ending punctuation
    print(found_loc)
    if found_loc >= 0:
        punc_loc = text.find('?', found_loc)
        print(punc_loc)
        if punc_loc >= 0:
            # Part 3: Create title string from tweet
            title_str = text[found_loc+len_needed_string+1:punc_loc]
            return title_str
        else:
            return 0
    else:
        is_question = text.find('?')
        if is_question == -1:
            return is_question
        else:
            return 0


def linear_interp_nodes(x_coords, y_coords, num_nodes):
    # Accepts 2 arrays of 2 values and create a random line
    # between the 2 using num_nodes.
    x = np.round(np.linspace(x_coords[0], x_coords[1], num_nodes))
    y = np.interp(x, x_coords, y_coords)
    # Add a value to the y so it isn't a straight line
    y_final = np.zeros(len(x))
    for each in range(len(x)):
        y_add = random.gauss(0,10)
        if y[each]+y_add > 50:
            y_final[each] = 50
        elif y[each]+y_add < -50:
            y_final[each] = -50
        else:
            y_final[each] = np.round(y[each]+y_add)
    return [x,y_final]


def create_graph(title):
    # Start with the end point
    end_vibe = random.randint(-50,50)
    start_val_rand = random.randint(-50,50)
    start_val = np.clip(start_val_rand, -50, 50)
    # Now I need to create an array of psuedorandom vals in between
    nodes = linear_interp_nodes([0,100],[start_val,end_vibe],40)
    # Now Chart them nice and pretty
    fig = plt.figure()
    plt.plot(nodes[0], nodes[1])
    plt.title(title, loc='center', fontsize=23)
    plt.axis([-7,110,-55,55])
    #plt.axis('off')
    plt.text(-10,1,'Now', size=12)
    plt.text(105,1,'Future', size=12)
    plt.text(2,55,'Good', size=12)
    plt.text(2,-55,'Bad', size=12)
    ax = fig.add_subplot(1,1,1)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.plot(nodes[0], nodes[1])
    #plt.show()
    # Save file name with datetime
    now = datetime.datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    fig_path = '/home/evan/Documents/Software/bad-genie-twitter-bot/Images/'
    plt.savefig(fig_path+name, format='jpg')
    return(fig_path+name)

# Insert 5min cycle to check for new retweets
################## LOOP ###########################
def start_twitter_bot():
    j = True
    while j is True:
        # write small script to get last reply tweet id...
        my_tweet = api.user_timeline(count = 1)
        last_tweetid = my_tweet[0]._json['id']
        # Get mentions for main loop
        mentions = api.mentions_timeline(since_id = last_tweetid)
        tweet_text = []
        tweet_id = []
        tweeter_userid = []
        for i in range(len(mentions)):
            tweet_id.append(mentions[i]._json['id'])
            tweet_text.append(mentions[i]._json['text'])
            # Use api with file created by create graph..
            chart_title = check_tweet_code(tweet_text[i], 'what does the future hold for')
            ######## Add Syntax If - Statement to handle incorrect formatting #########
            if type(chart_title) == str:
                filename_img = create_graph(chart_title)
                #file = create_graph()
                status = 'Do with this information what you will.....'
                api.update_with_media(filename_img, status, in_reply_to_status_id = tweet_id[i], auto_populate_reply_metadata = True)
            else:
                if chart_title == -1:
                    break
                else:
                    api.update_status('Sorry, please use the format listed in my bio for a prediction',in_reply_to_status_id = tweet_id[i], auto_populate_reply_metadata = True)
            # newest tweets are first.....
        time.sleep(150) #5 min intervals between checking


start_twitter_bot()

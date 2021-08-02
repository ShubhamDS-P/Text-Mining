# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 19:43:30 2021

@author: Shubham
"""

# sentiment analysis which parses the tweets fetched from twitter using python
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#load the data
from google.colab import files 
uploaded = files.upload()


# get the data
log = pd.read_csv('login.csv')  # reading the uploaded credential file

# Twitter API credentials
consumerKey = log['key'][0]
consumerSecret = log['key'][1]
accessToken = log['key'][2]
accessTokenSecret = log['key'][3]
------------------------
# Create the authentication object
authenticate = tweepy.OauthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Create the API object while passing in the auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)
------------------------------------
# Choosing the tweeter account ---we will choose the billgates tweeter account of bill and millanigates foundation

# Extract 100 tweets from the tweitter user
posts = api.user_timeline(screen_name = "BillGates", count = 100, lang "eng", tweet_mode= "extended")
print("Show the 5 recent tweets: \n")
i = 1
for tweet in posts[0:5]:
	print(str(i)+')'+tweet.full_text + '\n')
	i = i + 1
-----------------------------
# Create a dataframe with a column called tweets
df = pd.DataFrame([tweet.full_text for tweet in posts] , columns = ['Tweets'])

#Show the first 5 rows of data
df.head()
----------------------
# Clean the text
# Create a function to clean the tweets 
def cleanTxt(text):
	text = re.sub(r'@[A-Za-z0-9]+', '', text) # Removed @mentioned
	text = re.sub(r'#', '', text) # Removing the '#' symbol
	text = re.sub(r'RT[\s]+', '',text) # Removing RT
	text = re.sub(r'https?:\/\/\S+','',text) # Removing the hyper link
	return text

# Cleaning the text
df['Tweets'] = df['Tweets'].apply(cleanTxt)

# Show the cleaned text
df
----------------------
# Create a function to get the subjectivity 
def getSubjectivity(text):
	return TextBlob(text).sentiment.subjectivity

# Create a function  to get the polarity
def getPolarity(text):
	return TextBlob(text).sentiment.polarity

# Create two new columns
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

# Show the new dataframe with the new columns
df
-------------------------------------------------
# Plot the Word Cloud
allWords = ' '.join(twts for twts in df['Tweets']])
wordCloud = wordCloud(width = 500, height = 300, random_state = 21, max_font_size = 119).generate(allWords)

plt.imshow(WordCloud, interpolation = "billinear")
plt.axis('off')
------------------------------
# Create a function to compute the negative, neutral and positive analysis
def getAnalysis(score):
	if score<0:
		return 'Negative'
	elif score == 0:
		return 'Neutral'
	else:
		return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

# Show the dataframe
df
-----------------------------------
# Print all of the positive tweets
j=1
sortedDF = df.sort_values(by=['Polarity'])
for  in range(0, sortedDF.shape[0]):
	if(sortedDF['Analysis'][i] == 'Positive'):
		print(str(j) +') '+sortedDF['Tweets'][i])
		print()
		j = j+1
------------------------------------------------------
# Print the negative Tweets
j = 1
sortedDF = df.sort_values(by=['Polarity'], ascending = 'False')
for i in range(0, sortedDF.shape[0]):
	if(sortedDF['Analysis'][i] == 'Negative'):
	print(str(j)+') ' + sortedDF['Tweets'][i])
	print()
	j = j+1
-----------------------------------------------------
# Plot the polarity and subjectivity
plt.figure(figsize = (8,6))
for i in range(0, df.shape[0]):
	plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color = 'Blue')

plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()
----------------------------------------------
# Get the percentage of the positive tweets
ptweets = df[df.Analysis == 'Positive']
ptweets = ptweets['Tweets']

round((ptweets.shape[0] /df.shape[0])*100, 1)
---------------------------------------------------
# Get the percentage of negative tweets
ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets[Tweets']

round((ntweets.shape[0]/df.shape[0]*100) ,1)
-----------------------------------------------
# Show the value counts

df['Analysis'].value_counts()

#plot and visualize the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind= 'bar')
plt.show()
-------------------------------
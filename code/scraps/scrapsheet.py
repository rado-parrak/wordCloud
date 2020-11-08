'''
Created on Apr 11, 2019

@author: radov
'''
import datetime

# from newsapi import NewsApiClient
# 
# # Init
# newsapi = NewsApiClient(api_key='90bc20363ef04effb1550015111d18f2')
# 
# # /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(category='sports', language='cz', country='cz')
# 
# print(top_headlines)

# /v2/everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2017-12-01',
#                                       to='2017-12-12',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)

print(str(datetime.datetime.now().replace(microsecond=0)).replace(" ","'T'"))
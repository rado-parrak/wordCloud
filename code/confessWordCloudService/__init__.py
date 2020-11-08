'''
Created on Apr 12, 2019

@author: Radovan Parrak, Credo Analytics
'''
import codecs
import time
from geneeaAPI import callGeneea
from random import randint
from elasticsearch import Elasticsearch
import datetime, timedelta

class ConfessWordCloudService(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    def mockInputData(self, pathToFile, bufferLimit):
        # import data
        rawText = codecs.open(pathToFile, "r", encoding='utf-8').read()
        
        # mock newspaper articles
        self.articles = []
        article = ""
        verses = rawText.split("#")
        
        counter = 0
        articleCounter = 0
        for verse in verses:
            if counter > bufferLimit:
                self.articles.append(article)
                articleCounter += 1
                print("News article " + str(articleCounter) + " | " + article)
                
                article = verse
                counter = 0
                
            else:
                article = article + " " + verse
            counter += 1
    
    def analyzeInGeneea(self, MinWaitTime, MaxWaitTime):
        # prepare ES index
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        # create index if not already there
        self.elasticSearch_create_index(es, index_name='news_article_tags')
        self.elasticSearch_create_index(es, index_name='news_articles')
                
        counter = 0
        for article in self.articles:
            time.sleep(randint(MinWaitTime, MaxWaitTime))
            
            #if counter < 20:
            print("Analyzing in Geneea... Article : " + str(counter))
            result = callGeneea({'text': article})
            print("Storing result to Elastic...")
            self.storeToElastic(result, es)
            print("Result stored succesfully!")
            counter += 1
        
    def storeToElastic(self, genneaResult, es):
        # store articles
        articleResult = dict()
        timeStamp = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=2)
        articleResult['downloadTime'] = str(timeStamp.isoformat())
        print(articleResult['downloadTime'])
        articleResult['numberOfTags'] = genneaResult['tags'].__len__()
        self.elasticSearch_store_record(es, 'news_articles', articleResult)
        
        # store tags
        for tag in genneaResult['tags']:
            tagg = dict()
            timeStamp = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=2)
            tagg['analysisTime'] = str(timeStamp.isoformat())
            tagg['tag'] = tag['stdForm']
            tagg['relevance'] = tag['relevance']
            
            self.elasticSearch_store_record(es, 'news_article_tags', tagg)
        
                
    def elasticSearch_create_index(self,es_object, index_name):
        created = False
        # index settings
        if(index_name == 'news_article_tags'):            
            settings = {
                "mappings": {
                    "_doc": {
                        "dynamic": "strict",
                        "properties": {
                            "analysisTime" : {
                                "type":   "date",
                                "format": "date_hour_minute_second"
                                },
                            "tag" : { "type" : "keyword" },
                            "relevance" : { "type" : "double" }                                              
                        }
                    }
                }
            }
        if(index_name == 'news_articles'):            
            settings = {
                "mappings": {
                    "_doc": {
                        "dynamic": "strict",
                        "properties": {
                            "downloadTime" : {
                                "type":   "date",
                                "format": "date_hour_minute_second"
                                },
                            "numberOfTags" : { "type" : "double" }                                             
                        }
                    }
                }
            }
        try:
            if not es_object.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                es_object.indices.create(index=index_name, ignore=400, body=settings)
                print('ElasticSearch | created index: '+ index_name)
                created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created 
        
    def elasticSearch_store_record(self, elastic_object, index_name, record):
        try:
            elastic_object.index(index=index_name, doc_type='_doc', body=record)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))   
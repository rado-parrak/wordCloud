'''
Created on May 31, 2019

@author: radov
'''
import pandas as pd
from elasticsearch import Elasticsearch

class EsScorePersitor(object):
    '''
    classdocs
    '''


    def __init__(self, df):
        '''
        Constructor
        '''
        self.df = df # pandas df to be stored
        
        
    def fireUpEsSession(self, host, port):
        # create session
        self.es = Elasticsearch([{'host': str(host), 'port': str(port)}])
        
        # create 'scores' index:
        self.elasticSearch_create_scores_index()
    
    def elasticSearch_create_scores_index(self):
        created = False
        # index settings           
        settings = {
            "mappings": {
                "_doc": {
                    "dynamic": "strict",
                    "properties": {
                        "scoredObjectId" :{ "type" : "string" }, 
                        "scoreDateTime" : {
                            "type":   "date",
                            "format": "date_hour_minute_second"
                            },
                        "score" : { "type" : "double" },
                        "event" : { "type" : "double" },
                        "model" : {"type" : "keyword"},
                        "model_regime" : {"type" : "keyword"}                                             
                    }
                }
            }
        }
        try:
            if not self.es.indices.exists('scores'):
                # Ignore 400 means to ignore "Index Already Exist" error.
                self.es.indices.create(index='scores', ignore=400, body=settings)
                print('ElasticSearch | created index: Scores')
                created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created 
        
    def elasticSearch_store_record(self, record):
        try:
            self.es.index(index='scores', doc_type='_doc', body=record)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex)) 
        
    def storeToElastic(self):
        for row in self.df.to_dict('records'):
            print(row)
            self.elasticSearch_store_record(row)
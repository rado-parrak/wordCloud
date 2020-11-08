'''
Created on May 31, 2019

@author: radov
'''

import pandas as pd
import numpy as np
import datetime
from scraps import es_score_persistence
from scraps.es_score_persistence import EsScorePersitor

d = {'scoredObjectId': ['id1', 'id2', 'id3']
      , 'scoreDateTime': [str(datetime.datetime.now().replace(microsecond=0)), str(datetime.datetime.now().replace(microsecond=0)), str(datetime.datetime.now().replace(microsecond=0))]
      , 'score' : [0.65, 0.25 , 0.12]
      , 'event' : [1, 0 , 0]
      , 'model' : ['a', 'b', 'c']
      , 'model_regime' : ['batch', 'batch', 'real-time']
      }
 
df = pd.DataFrame(data=d)

# es = EsScorePersitor(df)
# es.fireUpEsSession("localhost", "9200")
# es.storeToElastic()

# df_dict = df.to_dict('records')
# 
# for el in df_dict:
#     print(el)

predicted = np.array([[0.65, 0.25], [0.65, 0.12], [0.25, 0.98]])
print(predicted)

scores = pd.DataFrame(df['scoredObjectId'])
scores['scoreDateTime'] =str(datetime.datetime.now().replace(microsecond=0))
scores['score'] = predicted[:,1]
scores['event'] = np.where(scores['score'] > 0.20 , 1, 0)
scores['model'] = 'python_xboost'
scores['model_regime'] = 'batch'

print(scores.head())
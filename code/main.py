# -*- coding: utf-8 -*-
'''
Created on Apr 11, 2019

@author: Radovan Parrak, Credo Analytics, All rights reserved
'''
from confessWordCloudService import ConfessWordCloudService

cwc = ConfessWordCloudService()
cwc.mockInputData(pathToFile = "R:/01_Analytics/confessWordCloud/03_data/bozska_komedie.txt", bufferLimit=15)
cwc.analyzeInGeneea(MinWaitTime = 0, MaxWaitTime = 3)


print("over and out!")
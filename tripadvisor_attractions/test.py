# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 04:47:29 2019

@author: hongj
"""

import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('review_crawler.py'))))
import review_crawler as rc
import multiprocessing as mp

if __name__== '__main__':
    spot_info= pd.read_csv('../results/spot_info.csv', encoding= 'utf-8', sep= ',')

    pool= mp.Pool(processes= mp.cpu_count())
    results= [pool.apply(rc.get_review, args= (spot_info.url[i], 
                                               spot_info.spot[i])) \
              for i in range(0, len(spot_info))]
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 04:14:39 2019

@author: hongj
"""

from crawler import tripadvisor_attraction_crawler as tac
import multiprocessing as mp
#import pandas as pd


def main(driver_directory, url):
    
    crawler= tac.review_crawler(driver_directory, url)
    crawler.execute()
    
    
if __name__== '__main__':
    
    driver_directory= '../chromedriver.exe'
    
    url_list= tac.get_attraction_url_list(driver_directory= driver_directory, 
                                          base_url= 'https://www.tripadvisor.co.za/Attractions-g294197-Activities-Seoul.html',
                                          num= 100)
    
    url_list= [(driver_directory, url) for url in url_list]
    
    n_cpu= mp.cpu_count()
    
    mp.freeze_support()
    with mp.Pool(processes= n_cpu) as pool:
        pool.starmap(main, url_list)
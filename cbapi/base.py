#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 23:52:23 2020

@author: nick
"""


# %%% imports

import requests
import threading
import json
import pandas as pd
import os
import datetime

# %%% constants

url_org = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"
url_ppl = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

host = "crunchbase-crunchbase-v1.p.rapidapi.com"

headers = {
    'x-rapidapi-host': host,
    'x-rapidapi-key': os.environ.get("CBAPI_KEY")
    }

# %%% class definitions

class Response:
    """
    Simple wrapper class for the json dictionary one get as a response
    from the api, this makes retrieving the required data a bit easier and
    reusable
    """
    
    # constructor
    def __init__(self, json_str):
        self.resp = json.loads(json_str)
    
    # get number of pages
    def number_pages(self):
        return self.resp["data"]["paging"]["number_of_pages"]
    
    # get items, maybe as dataframe
    def get_items(self):
        df = pd.DataFrame() # initalize return dataframe
        #iterate over all items in the response and append them
        for it in self.resp["data"]["items"]:
            df = df.append(it["properties"], ignore_index=True)
        
        return df
            
# %%% functions

def timestamp2datetime(x):
    """ simple function to convert timestamp to datetime"""
    return datetime.datetime.fromtimestamp(x)

def get_page(url, page: int, result=None, index=None, filters=None):
    """
    loads one specific page of the organizatzion or people result, if result list is
    provided, then result is stored at the specified index insted of returned
    """
    if filters is None:
        filters = {"page": page}
    else:
        filters["page"] = page
    
    
    req_str = requests.request("GET", url, headers=headers, params=filters)
    
    # return the result if not storage list is provided
    if result is None:
        return Response(req_str.text).get_items()
    else:
        result[index] = Response(req_str.text).get_items()


def get_organizations(updated_since = None, query = None, name = None,
                      domain_name = None, locations = None, page = None,
                      page_limit = 20):
    
    # create the filter dictionary
    filters = {
        "updated_since": updated_since.timestamp() if type(updated_since) == datetime.datetime else None,
        "query" : query,
        "name": name,
        "domain_name": domain_name,
        "locations": locations,
        "page": page
        }
    
    # get the first page for this request
    req_str = requests.request("GET", url_org, headers=headers, params=filters) # add the parameters here
    resp = Response(req_str.text)
    
    # the first page as a dataframe
    df = resp.get_items()
    
    # check how many pages there are
    nb_pages = resp.number_pages()
    
    # check if page was given as filter
    if page is None and nb_pages > 1:
        # get the rest of the pages using mutliple threads
        
        # limit the number of pages
        if page_limit is not None:
            nb_pages = min(resp.number_pages(), page_limit) 
        
        # initiailze two lists, one to stroe the results and one for the threads
        page_list = [None]*(nb_pages-1)
        thread_list = [None]*(nb_pages-1)
        # start the threads
        for i in range(nb_pages-1):
            thread_list[i] = threading.Thread(target=get_page, args=(url_org, i+1, page_list, i, filters))
            thread_list[i].start()
        # join threads and combinde results into a single dataframe
        for i in range(nb_pages-1):
            thread_list[i].join()
            df = df.append(page_list[i], ignore_index=True)
    
    # change timestamps to datetime dates
    if df.shape[0] > 0:
        for col in ["created_at", "updated_at"]:
            df[col] = df[col].apply(timestamp2datetime)
    
    return df


def get_people(name = None, query = None, updated_since = None, 
               locations = None, page = None, 
               page_limit = 20):
    
    # create the filter dictionary
    filters = {
        "updated_since": updated_since.timestamp() if type(updated_since) == datetime.datetime else None,
        "query" : query,
        "name": name,
        "locations": locations,
        "page": page
        }
    
    # get the first page for this request
    req_str = requests.request("GET", url_ppl, headers=headers, params=filters) # add the parameters here
    resp = Response(req_str.text)
    
    # the first page as a dataframe
    df = resp.get_items()
    
    # check how many pages there are
    nb_pages = resp.number_pages()
    
    # check if page was given as filter
    if page is None:
        # get the rest of the pages using mutliple threads
        
        # limit the number of pages if wanted
        if page_limit is not None:
            nb_pages = min(resp.number_pages(), page_limit) 
        
        # initiailze two lists, one to stroe the results and one for the threads
        page_list = [None]*(nb_pages-1)
        thread_list = [None]*(nb_pages-1)
        # start the threads
        for i in range(nb_pages-1):
            thread_list[i] = threading.Thread(target=get_page, args=(url_ppl, i+1, page_list, i, filters))
            thread_list[i].start()
        # join threads and combinde results into a single dataframe
        for i in range(nb_pages-1):
            thread_list[i].join()
            df = df.append(page_list[i], ignore_index=True)
    
    # change timestamps to datetime dates
    if df.shape[0] > 0:
        for col in ["created_at", "updated_at"]:
            df[col] = df[col].apply(timestamp2datetime)
    
    return df

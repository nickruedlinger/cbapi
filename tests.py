# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 21:39:10 2020

@author: nick
"""

# %%%
import cbapi

# simple base version, without filters
org1 = cbapi.get_organizations()
ppl1 = cbapi.get_people()

# %%%

# test full text search
org2 = cbapi.get_organizations(query = "test")


# %%% test page limit

org3 = cbapi.get_organizations(page_limit = 3)
ppl3 = cbapi.get_people(page_limit = 2)




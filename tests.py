# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 21:39:10 2020

@author: nick
"""

# %%%
import cbapi
import datetime

# simple base version, without filters
org1 = cbapi.get_organizations()
ppl1 = cbapi.get_people()

# %%% test filters

# test full text search
org2 = cbapi.get_organizations(query = "test")
ppl2 = cbapi.get_people(query = "manager")


# test multiple filters together
org4 = cbapi.get_organizations(name = "bexio", locations="Rapperswil")
ppl4 = cbapi.get_people(name="Oliver",updated_since=datetime.datetime(2020, 8, 1))

# %%% test page limit

org3 = cbapi.get_organizations(page_limit = 3)
ppl3 = cbapi.get_people(page_limit = 2)




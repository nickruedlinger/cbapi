# Crunchbase Python API

by: Nick Rüdlinger


## Setup

### Crunchbase API Key
To use the cbapi package, one needs to have his own private crunchbase aip key. The key needs to be set as an environment variable called
*CBAPI_KEY*.

## Functions
The package contains two simple functions to access the two free access points of the crunchbase api.

### Retrieve Organization data

```Python
cbapi.get_organizations(updated_since = None, query = None, name = None,
                      domain_name = None, locations = None, page = None,
                      page_limit = 20)
```

all parameters are optional:

- updated_since: *datetime*, only return entries that were updated since than
- query: *string*, full text search filter on companies name, alias and description
- name: *string*, filter for a companies name
- domain_name: *string*, filter for a companies domain_name
- locations: *string*, filter for locations, multiple are possible if comma separated (e.g. 'Zurich,Rome') but are logical AND.
- page: *int*, search for a specific page in the results
- page_limit: *int*, limit number of pages returned, to keep thins fast, default is 20

returns a pandas dataframe containig all the properties for the different companies

### Retrieve People data

```Python
cbapi.get_people(name = None, query = None, updated_since = None,
               locations = None, page = None,
               page_limit = 20)
```
all parameters are optional:

- name: *string*, filter for a companies name
- query: *string*, full text search filter on companies name, alias and description
- updated_since: *datetime*, only return entries that were updated since than
- locations: *string*, filter for locations, multiple are possible if comma separated (e.g. 'Zurich,Rome') but are logical AND.
- page: *int*, search for a specific page in the results
- page_limit: *int*, limit number of pages returned, to keep thins fast, default is 20

returns a pandas dataframe containig all the properties for the different people

## Installation

The package can be installed directly from github. To do so, simply run:
```
pip install git+https://github.com/nickruedlinger/cbapi.git
```

#!/usr/bin/env python
# coding: utf-8

#Set Up the ETL Environment
###API & Pandas Requirements
import requests
import pandas as pd
import sys
from pandas.io.json import json_normalize
from datetime import datetime
import gc

###Database Connection Details
### Detailed info on connecting to BigQuery: https://cloud.google.com/bigquery/docs/pandas-gbq-migration
#
full_table_id = 'XXXXXXXXXXX'
#
project_id = 'XXXXXXXXXXX'

url = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"

q_check_contents = """SELECT max(last_system_update_date) as last_system_update_date FROM testproject_213618.citibike_data"""

def request_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Data Source Server Status Issue ")
        gc.collect()
        sys.exit()
    else:
        print("Server Status Shows New Update ")
        pass
    return r

def construct_dataframe(r):
    stations = r.json()['data']['stations']
    last_updated = r.json()['last_updated']

    dt_object = datetime.fromtimestamp(last_updated).strftime('%Y-%m-%d %H:%M:%S')
    print("Last Updated: " + str(dt_object))

    df = json_normalize(stations)
    df['last_system_update_date'] = dt_object
    df['insertion_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\nData For Insertion Constructed ")
    return df

def insert_data(df):
    df.to_gbq(full_table_id, project_id=project_id,if_exists='append')
    print("\nData Insertion Time: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    return

def check_contents(r,df,mq_check_contents=q_check_contents,project_id=project_id):
    d = pd.read_gbq(q_check_contents,project_id=project_id)
    #last system update record in the database
    last_system_update_date = d['last_system_update_date'][0]
    #last system update reported by the server response
    last_updated = datetime.fromtimestamp(r.json()['last_updated']).strftime('%Y-%m-%d %H:%M:%S')
    #check if the last_system_update_date entered in the database is less than the current date.
    #if it is not, do not insert the new data as you'll be adding duplicative records
    if last_system_update_date > last_updated:
        print("\nData not inserted due to duplicative records ")
        gc.collect()
        sys.exit()
    else:
        print("\nData does not contain duplicate records ")
        insert_data(df)
    return

r = request_data(url)
df = construct_dataframe(r)
## Below function to be run only once on the first insertion of data into the new table
#insert_data(df)
check_contents(r,df)
gc.collect()

#run me every minute in cron:
#set your local editin environment to nano
#https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx.html
#env EDITOR=nano crontab -e
#insert the below with updated file path into crontab
#* * * * * /PATH/the_name_of_this_file.py
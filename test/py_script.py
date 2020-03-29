#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 14:14:15 2020

@author: andy.owens
"""

import pandas as pd
import datetime

file_name = "https://people.sc.fsu.edu/~jburkardt/data/csv/homes.csv"
df = pd.read_csv(file_name)

df.to_csv("test_output"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+".csv")
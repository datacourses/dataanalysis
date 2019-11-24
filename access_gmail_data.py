#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 17:03:43 2017

@author: andyowens
"""

import pandas as pd
import datetime, os, glob

cwd = os.getcwd()

EMAIL_UN = 'awowens06@gmail.com'
EMAIL_PW = 'iluxfwnbimmuqoxh'

subject_header = "Google Analytics: Page Performance"

def get_files(path,ftype):
    os.chdir(path)
    files = [f for f in glob.glob("*"+str(ftype))]
    dfiles = pd.Series(files)
    return dfiles

def details(subject_header,date=(datetime.datetime.now()-datetime.timedelta(1)).strftime("%d-%b-%Y")):
    #EMAIL SEARCH CRITERIA
    search_criteria = '(ON '+date+' SUBJECT "'+subject_header+'")'
    return search_criteria

def attachment_download(SUBJECT):
    import email, imaplib
    un = EMAIL_UN
    pw = EMAIL_PW
    url = 'imap.gmail.com'

    detach_dir = '.' # directory where to save attachments (default: current)
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL(url,993)
    m.login(un,pw)
    m.select() 
    resp, items = m.search(None, SUBJECT)
    # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    
    items = items[0].split() # getting the mails id
    
    for emailid in items:
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        email_body = data[0][1] # getting the mail content
        mail = email.message_from_string(str(email_body)) # parsing the mail content to get a mail object
    
        #Check if any attachments at all
        if mail.get_content_maintype() != 'multipart':
            continue
    
        print("["+mail["From"]+"] :" + mail["Subject"])
    
        # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue
    
            # is this part an attachment:
            if part.get('Content-Disposition') is None:
                continue
    
            filename = part.get_filename()
            counter = 1
    
            # if there is no filename, we create one with a counter to avoid duplicates
            if not filename:
                filename = 'part-%03d%s' % (counter, 'bin')
                counter += 1
    
            att_path = os.path.join(detach_dir, filename)
    
            #Check if its already there
            if not os.path.isfile(att_path):
                # finally write the stuff
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        print(str(filename)+ ' downloaded')
        return filename

def open_csv_file(file_name):
    #WIP - GET EMAIL ALERT TIME DOWN
    #READ FILE
    df = pd.read_csv(os.getcwd()+"/"+file_name,encoding='utf-8',skiprows=9)
    return df

i = 0
c = details(subject_header,date=(datetime.datetime.now()-datetime.timedelta(i)).strftime("%d-%b-%Y"))

file_name = attachment_download(c)

df = open_csv_file(file_name)

#df = format_transform(df)
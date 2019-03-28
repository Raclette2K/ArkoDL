##########################
# Arkotheque downloader
# Copyright © 2019 Pierre Boisselier
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.
##########################

# DISCLAIMER :
# See README.txt
# LICENSE :
# See README.txt
# NB: 
# This is a less-than-a-day work, it can be buggy and could not 
# work anymore for whatever reason. The code is badly written, I'm 
# not a Python guy and it was made in the first place for improving myself
# in python.
# What even if the use of this thing ?
# Figure it out yourself.


import re
import urllib.request
import os
import random


def extractID(file):
    ids=[]
    for i in re.findall('data-cle-image="(.+?)"',file):
        if not i in ids:
            ids.append(i)
    return ids

def extractCote(file):
    cote = re.findall('data-cote="(.+?)"',file)
    if len(cote) > 1 :
        if cote[1]!='" data-arklink=':
            return cote[1].replace(" ","")
    else:
        return "tmp_"+str(random.randint(100,10000)*7) # If no number, generate a random one

def generateURL(ids, dom):
    urls=[]
    for i in ids:
       urls.append("http://"+dom+"/arkotheque/visionneuse/img_prot.php?i="+i+".jpg")
    return urls
            
def openURL(url):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'user-Agent' : user_agent }
    req = urllib.request.Request(url,None,headers)
    res = urllib.request.urlopen(req)
    ckie = res.headers.get('Set-Cookie')
    page = res.read()
    res.close()
    return [page.decode(encoding='UTF-8',errors='ignore'),ckie]

def downloadFile(url,filename,ckie):
    req = urllib.request.Request(url)
    req.add_header('cookie',ckie)
    res = urllib.request.urlopen(req)
    if not os.path.exists(filename):
        with open(filename,'wb') as f:
            f.write(res.read())
    res.close()
    print(filename+" was downloaded!")
    return None

def downloadAll(id_url, ckie, path):
    index = 0
    for i,u in id_url.items():
        downloadFile(u,os.path.join(path,str(index)+"_"+i)+".jpg",ckie)
        index+=1


def getArchive(url,path="vol"):
    if "arkotheque" not in url:
        raise ValueError("The URL provided is not an arkotheque link!")
    
    dom = urllib.parse.urlsplit(url)[1]
    page = openURL(url)
    ids=extractID(page[0])
    folder = extractCote(page[0])
    path = os.path.join(path,folder)
    if not os.path.exists(path):
        os.makedirs(path)
    print("Downloading book "+folder+" in "+path+"...")
    urls = generateURL(ids,dom)
    id_url = dict(zip(ids,urls))
    downloadAll(id_url,page[1],path)
    print("Done!")



while(True):
    usrin = input("Enter an arkotheque URL: ")
    try:
        getArchive(usrin)
        break;
    except ValueError as err:
        print(err.args[0])



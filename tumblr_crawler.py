print "Program Started"

import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import requests
import shutil
import re
import sys
import math


#DEFINE THE FUNCTIONS WE NEED

def enlarge_tumblr_pic(archive_url, size):
    if size is 'large' or 'L':
        if (requests.get(archive_url.replace('_250','_1280',1))).status_code < 400:
            new_url = archive_url.replace('_250','_1280',1)
        elif (requests.get(archive_url.replace('_250','_500',1))).status_code < 400:
            new_url = archive_url.replace('_250','_500',1)
        else:
            new_url =   archive_url 
    elif size is 'medium' or 'M':
        if (requests.get(archive_url.replace('_250','_500',1))).status_code < 400:
            new_url = archive_url.replace('_250','_500',1)
        else:
            new_url =   archive_url 
    elif size is 'small' or 'S':
        new_url =   archive_url                 
    return new_url

#enlarge_tumblr_pic('http://38.media.tumblr.com/a68e4902b439b8f7e4add5be9091387f/tumblr_mqjz0tj6w21qdlh1io1_250.gif',"L")

        
#Strip the image urls from the page source code
def get_image_urls(page_url):
    r = requests.get(page_url)
    url_list = [] #contains just pics
    for line in (''.join(r.text)).splitlines():
        if '''imageurl''' in line:
            try:
                dirty_url_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(line)) #contains pics + blogs
                if  len(dirty_url_list) != 0:
                    for url in dirty_url_list:
                        if "media" in url:
                            url_list.append(str(url)) 
            except UnicodeEncodeError:
                print "Fix the fucking Unicode error"
    return url_list
    
    
#Strip the image urls from the page source code
def month_has_posts(page_url):
    page_has_posts = True
    r = requests.get(page_url)
    for line in (''.join(r.text)).splitlines():
        if '''No posts yet.''' in line:
            page_has_posts = False
    return page_has_posts    

#Download the actual picuture:
def get_image(url,filename): #get_image(string for url, string for filename on local computer)
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)    
    del response
    return
    


#BEGIN THE ACTUAL PROGRAM:

base_url = 'http://otarsface.tumblr.com/' #link to your tumblr blog

picture_urls = [] #list of all picture URLs to download

#Find the links to the pictures we want to download:
print "Find the links to the pictures"

import datetime
current_month = int(datetime.date.today().strftime("%m"))
current_year = int(datetime.date.today().strftime("%Y"))
page_has_posts = True
month,year = current_month,current_year

#Search the archive
while page_has_posts:

    print month, year
    
    page_url = base_url + "archive/"+str(year)+"/"+str(month)
    print page_url    
    print "Month has posts?", month_has_posts(page_url)
    
    picture_urls.extend(get_image_urls(page_url)) #get the actual image links   
    
    month = month - 1
    
    if month == 0:
        month = 12
        year = year - 1       

    #Failsafe
    if month < 8 or year < 2015:
        break
        
num_images = len(picture_urls)        
print "Total images:", num_images

#Enlarge the images if possible
print "Attemp to enlarge images", num_images
temp_urls = []
for indx, url in enumerate(picture_urls):
    sys.stdout.write('\r')
    sys.stdout.write("%d%% complete" % (int(((indx+1)/float(len(picture_urls)))*100)))
    sys.stdout.flush()
    temp_urls.append(str(enlarge_tumblr_pic(url,"L")))
picture_urls = temp_urls
sys.stdout.write('\n')

#Write the list of urls to file
with open(os.path.join(__location__,"image_links.txt"),"w") as file:
    for url in picture_urls:
        file.write(str(url)+"\n")


#Download the pictures:  
print "Begin download of",len(picture_urls)+1,"pictures"   
download_size = 0 #bytes   
bypassed = 0
for indx, url in enumerate(picture_urls):
    filename = os.path.join(__location__, (url.split("/")[-1])) #fname is last subtree of tumblr url
    if not os.path.exists(filename): 
        get_image(url,filename)
        sys.stdout.write('\r')
        sys.stdout.write("%d%% complete" % (int(((indx+1)/float(len(picture_urls)))*100)))
        sys.stdout.flush()
        download_size = download_size + os.path.getsize(filename) #bytes
    else:
      bypassed += 1  


if indx > 0:
    print "\nDownload of",(indx+1)-bypassed,"images complete"
    print bypassed,"images skipped"   
    print "Total Size:",(download_size/1000000),"mb"
    print "Average Size:",(download_size/float(indx))/1000,"kb"
else:
    print "no pics downloaded"

    

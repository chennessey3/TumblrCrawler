print "Program Started"

import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import requests
import shutil
import re
import sys

#DEFINE THE FUNCTIONS WE NEED

def enlarge_tumblr_pic(archive_url):
    if (requests.get(archive_url.replace('_250','_1280',1))).status_code < 400:
        new_url = archive_url.replace('_250','_1280',1)
    elif (requests.get(archive_url.replace('_250','_500',1))).status_code < 400:
        new_url = archive_url.replace('_250','_500',1)
    else:
       new_url =   archive_url   
    return new_url

enlarge_tumblr_pic('http://38.media.tumblr.com/a68e4902b439b8f7e4add5be9091387f/tumblr_mqjz0tj6w21qdlh1io1_250.gif')

#Figure out what kind of image file the url links to
def get_image_type(url):
    if '.png' in url:
        filetype = '.png'
    elif '.jpg' in url:
        filetype = '.jpg'
    elif '.gif' in url:
        filetype = '.gif'            
    else:
        print "unknown file type"
        filetype = '.ERROR'   
        
    return filetype
        
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
    
#url = 'http://36.media.tumblr.com/ef10cb3dc022c1a0f6e6e361c2d33cf5/tumblr_noj473Sgbo1sn75h6o1_500.jpg'
#filename = os.path.join(__location__, 'test_image3.png')    
#get_image(url,filename)

#BEGIN THE ACTUAL PROGRAM:

base_url = 'http://otarsface.tumblr.com/' #link to your tumblr blog

picture_urls = [] #list of all picture URLs to download

#Find the links to the pictures we want to download:
print "Find the links to the pictures"

import datetime
current_month = int(datetime.date.today().strftime("%m"))
current_year = int(datetime.date.today().strftime("%Y"))
print current_month,current_year
page_has_posts = True
month_counter,year_counter = 0,0
month,year = current_month,current_year

while page_has_posts:

    print month, year
    
    page_url = base_url + "archive/"+str(year)+"/"+str(month)
    print page_url    
    print "Month has posts?", month_has_posts(page_url)

#    page_has_posts = month_has_posts(page_url)
    
    picture_urls.extend(get_image_urls(page_url))    
    
    month = month - 1
    
    if month == 0:
        month = 12
        year = year - 1       

    #Failsafe
    if month < 7 or year < 2008:
        break


#Download the pictures:  
print "Begin download of pictures"   
   
for indx, url in enumerate(picture_urls):
    filename = os.path.join(__location__, ("test_image" + str(indx) + get_image_type(url)))
#    print filename 
    get_image(url,filename)
#    print int((indx/float(len(picture_urls)))*100)
    sys.stdout.write('\r')
#    sys.stdout.write("[%-20s] %d%%" % ('='*(int(indx/len(picture_urls))*20), int((indx/len(picture_urls)*100))))
#    sys.stdout.write("[%-100s] %d%%" % ('='*int(100*(indx/len(picture_urls))), (indx/len(picture_urls))*100))
    sys.stdout.write("%d%% complete" % (int((indx/float(len(picture_urls)))*100)))
    sys.stdout.flush()

print "\nDownload of",indx,"images complete"   

with open(os.path.join(__location__,"image_links.txt"),"w") as file:
    for url in picture_urls:
        file.write(str(enlarge_tumblr_pic(url))+"\n")
    

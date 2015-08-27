print "Program Started"

import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import requests
import shutil
import re
import sys

#DEFINE THE FUNCTIONS WE NEED

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
        

def get_image_urls(page_url):
    r = requests.get(page_url)
    url_list = [] #contains just pics
    for line in (''.join(r.text)).splitlines():
        if '''<div class="media">''' in line:
            dirty_url_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(line)) #contains pics + blogs
            if  len(dirty_url_list) != 0:
                for url in dirty_url_list:
                    if "media" in url:
                        url_list.append(str(url)) 
    return url_list

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

#base_url = 'http://otarsface.tumblr.com/' #link to your tumblr blog
#base_url = 'http://totallynotapornblog.tumblr.com/' #link to your tumblr blog
base_url = 'http://shydaydream.tumblr.com/' #link to your tumblr blog

num_pages = 2 #number of pages to get images from

picture_urls = [] #list of all picture URLs to download

#Find the links to the pictures we want to download:
print "Find the links to the pictures"

for page_num in range(1,num_pages+1):
    page_url = base_url + "page/" + str(page_num)
#    print page_url
    r = requests.get(page_url)
#    print r.encoding
#    print r.status_code
    picture_urls.extend(get_image_urls(page_url))


#Download the pictures:  
print "Begin download of pictures"   
   
for indx, url in enumerate(picture_urls):
    filename = os.path.join(__location__, ("test_image" + str(indx) + get_image_type(url)))
#    print filename 
    get_image(url,filename)
    print int((indx/float(len(picture_urls)))*100)
#    sys.stdout.write('\r')
#    sys.stdout.write("[%-20s] %d%%" % ('='*(int(indx/len(picture_urls))*20), int((indx/len(picture_urls)*100))))
#    sys.stdout.write("[%-100s] %d%%" % ('='*int(100*(indx/len(picture_urls))), (indx/len(picture_urls))*100))
#    sys.stdout.flush()

print "\nDownload of",indx,"images complete"   

import codecs
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import requests
import shutil
import re

#view the page source:
url = 'http://otarsface.tumblr.com/page/40'
r = requests.get(url)
#print r.text

#print (r.text[10])
#print r.encoding

count = 0    
fid = codecs.open(os.path.join(__location__, 'output.log'), "w","utf-8-sig" )
        
for line in (''.join(r.text)).splitlines():
    if '''<div class="media">''' in line:
        url_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(line))
        if  len(url_list) != 0:
            for url in url_list:
                if "media" in url:
                    fid.write(str(url) + "\n") 
fid.close()        
print "number of images on page:", count

#Download the actual picuture:
url = 'http://41.media.tumblr.com/b006df86635b43d695e748bc99462eca/tumblr_nru6mcrkOp1sfxd21o1_500.png'
filename = os.path.join(__location__, 'test_image2.png')
response = requests.get(url, stream=True)
with open(filename, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
print response.status_code

del response





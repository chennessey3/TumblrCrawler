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
fid = open(os.path.join(__location__, 'output.log'), "w")
        
for line in (''.join(r.text)).splitlines():
    if '''<div class="media">''' in line:
#        print re.findall("(?P<url>https?://[^\s]+)", line), "\n\n"
        count = count + 1
        print count
        fid.write( str(line) + "\n") 
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


#Test url finder:
text = '''                        <div class="media"><img src="http://38.media.tumblr.com/2d50d4f036f4c787699b4a5f2ddaf2e6/tumblr_n8ze5zBEHw1r5pe9fo1_500.gif" alt="" /></div> '''
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
print urls



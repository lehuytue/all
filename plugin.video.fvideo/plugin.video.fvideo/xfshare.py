import xutils
import urllib2
from BeautifulSoup import BeautifulSoup
def getFileFromFolder(url):
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }      
    req = urllib2.Request(urllib2.unquote(url),headers=headers2)
    f = urllib2.urlopen(req)    
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)    
    items = soup.findAll('div', {'class': 'pull-left file_name'})
    ret = ''
    temp=''
    for item in items:
        link=item.a
        href = link['href']
        href = href.replace("http:","https:")
        name = link['title']
        icon = ""
        if ('.rar' in name) or ('.srt' in name):
            t=1
        else:
            try:
                if temp=='':
                    temp = '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
                else:
                    temp = temp + ',' + '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
            except:
                pass    
    ret = '{"items":['+temp+']}'
    return ret
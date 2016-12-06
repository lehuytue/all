import xutils
import urllib2
import urllib

from BeautifulSoup import BeautifulSoup
def getAll(url):
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }      
    req = urllib2.Request(urllib2.unquote(url),headers=headers2)
    f = urllib2.urlopen(req)    
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)    
    items = soup.findAll('div', {'class': 'entry-thumbnails'})
    pageNext = soup.find('a', {'class': 'page larger'})
    strNext = ""
    if pageNext <> None:
        strNext = pageNext['href']
    ret = ''
    temp=''
    for item in items:
        link=item.a
        href = link['href']
        #href = href.replace("http:","https:")
        name1 = link['title'][126:]
        if(name1==None) or (name1==""):
            name1=href
        lTemp = name1.split('</h3>')
        name = lTemp[0].replace("<br/>","")
        name = lTemp[0].replace("<br />","")
        icon = link.img['src']

        try:
            if temp=='':
                temp = '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
            else:
                temp = temp + ',' + '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
        except:
            pass    
    ret = '{"items":['+temp+'],"next":"'+strNext+'"}'
    return ret

def getLink(url):
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }      
    req = urllib2.Request(urllib2.unquote(url),headers=headers2)
    f = urllib2.urlopen(req)    
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)    
    items = soup.findAll('a')
    ret = ''
    temp=''
    temp1=''
    for item in items:
        try:
            href = item['href']
            href = href.replace("http:","https:")
            if href.find('fshare.vn/file')>0:
                name = item.text
                icon = ""

                if temp=='':
                    temp = '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
                else:
                    temp = temp + ',' + '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
                    
            if href.find('fshare.vn/folder')>0:
                name = item.text
                icon = ""

                if temp1=='':
                    temp1 = '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'
                else:
                    temp1 = temp1 + ',' + '{"name":"'+name+'","icon":"'+icon+'","href":"'+href+'"}'      
        except:
            pass    
    ret = '{"files":['+temp+'],"folders":['+temp1+']}'
    return ret

def searching(strInput):
    href = "http://vaphim.com/?s=" + strInput.strip()
    return getAll(urllib.quote_plus(href))
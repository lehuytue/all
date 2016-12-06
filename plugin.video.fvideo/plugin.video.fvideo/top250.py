URL_BASE = "http://akas.imdb.com/chart/top?ref=ft_250"
import xutils
import urllib2
from BeautifulSoup import BeautifulSoup
def getAll(iicon):
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }      
    req = urllib2.Request(urllib2.unquote(URL_BASE),headers=headers2)
    f = urllib2.urlopen(req)    
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)    
    tbody = soup.find('tbody', {'class': 'lister-list'})
    ret = ''
    temp=''
    trs = tbody('tr')
    for tr in trs:
        tds=tr('td')
        icon = ''
        title = ''
        for td in tds:
            if td['class']=='posterColumn':
                icon = td.a.img['src'].encode("utf-8")
            if td['class']=='titleColumn':
                title=td.a.text.encode("utf-8")
        try:
            if temp=='':
                temp = '{"name":"'+title+'","icon":"'+icon+'"}'
            else:
                temp = temp + ',' + '{"name":"'+title+'","icon":"'+icon+'"}'
        except:
            pass    
    ret = '{"items":['+temp+']}'
    return ret







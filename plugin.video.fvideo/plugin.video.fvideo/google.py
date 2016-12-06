import xutils
import urllib2
from BeautifulSoup import BeautifulSoup
SEARCH_URL='http://www.google.com.vn/custom?hl=en&q=site:fshare.vn/%s+%s&num=%s&start=%s&as_qdr=%s'
def search(url, query, type, page, searchnum):
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }
    ret = ''
    snext='0'
    if query is None or query=='':
        return ret
    url=SEARCH_URL % (type,query.replace(' ', '+'),searchnum,str(int(searchnum)*page),'all')  
    
    req = urllib2.Request(urllib2.unquote(url),headers=headers2)
    f = urllib2.urlopen(req)          
    soup = BeautifulSoup(str(f.read()), convertEntities=BeautifulSoup.HTML_ENTITIES)  
    results=soup.findAll('div', {'class': 'g'})
    findingNexts=soup.findAll('div', {'id': 'navbar'})

    for item1 in findingNexts:
        spans=item1.findAll('span')
        for item2 in spans:
            name=item2.text.encode("utf-8")
            if name=='Next':
                snext='1'
    elements = ''
    file = ''
    folder = ''
    for item in results:
        a=item.find('a')
        name=a.text.encode("utf-8").replace('  ',' ')
        href=a['href']
        thumb = ''
        date = ''
        duration = 0
        desc = ''

        try:
            sName = name
            #if ('.srt' in sName) or ('.rar' in sName) or ('Dich vu chia se' in sName):
            if ('.srt' in sName) or ('.rar' in sName):
                t=1
            else:
                if href.find('fshare.vn/file')>0:        
                    temp = '{"name":"'+sName+'","href":"'+href+'"}'
                    if file=='':
                        file = temp
                    else:
                        file = file + ',' + temp
                elif href.find('fshare.vn/folder')>0:
                    temp = '{"name":"[Folder] '+sName+'","href":"'+href+'"}'
                    if folder=='':
                        folder = temp
                    else:
                        folder = folder + ',' + temp
        except:
            pass  
    ret = '{"page":"'+str(page)+'","files":['+file+'],"folders":['+folder+'],"next":"'+snext+'"}'
    return ret
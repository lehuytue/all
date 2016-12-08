import xutils
import urllib2
from BeautifulSoup import BeautifulSoup


def getFileList():
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }      
    url = "https://raw.githubusercontent.com/taikhoanonlinevn/all/master/plugin.video.fvideo/plugin.video.fvideo/resources/000_list.txt"
    req = urllib2.Request(urllib2.unquote(url),headers=headers2)
    f = urllib2.urlopen(req)    
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)    
    lines = soup.text.split('\n')
    return lines

def getFilmList(vfilename):
    headers2 = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'
                ,'Accept-Language': 'en-US,en;q=0.5'
                }      
    ret = ''
    filetemp=''
    foldertemp=''
    url = "https://raw.githubusercontent.com/taikhoanonlinevn/all/master/plugin.video.fvideo/plugin.video.fvideo/resources/" + vfilename
    req = urllib2.Request(urllib2.unquote(url),headers=headers2)
    f = urllib2.urlopen(req)    
    soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)    
    lines = soup.text.split('\n')
    
    for line in lines:
        try:        
            list = line.split("##")
            href = list[1].strip()
            name = list[0].encode("utf-8")   
                
            if href.find('fshare.vn/file')>0:
                if filetemp=='':
                    filetemp = '{"name":"'+name+'","icon":"","href":"'+href+'"}'
                else:
                    filetemp = filetemp + ',' + '{"name":"'+name+'","icon":"","href":"'+href+'"}'
            elif href.find('fshare.vn/folder')>0:
                if foldertemp=='':
                    foldertemp = '{"name":"'+name+'","icon":"","href":"'+href+'"}'
                else:
                    foldertemp = foldertemp + ',' + '{"name":"'+name+'","icon":"","href":"'+href+'"}'            
        except:
            pass
          
    ret = '{"files":['+filetemp+'],"folders":['+foldertemp+']}'
    return ret
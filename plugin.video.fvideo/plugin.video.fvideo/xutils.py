import sys
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import urlfetch
import Cookie
import StorageServer
import xbmc
import cookielib

from BeautifulSoup import BeautifulSoup

base_url = sys.argv[0]
HTTP_DESKTOP_UA = {
    'Host':'www.fshare.vn',
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate',
    'Referer':'https://www.fshare.vn/login',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',    
    'Connection':'keep-alive'
}
headers=HTTP_DESKTOP_UA
cookie = None

def getSessionId(str):
    ret = ""
    try:
        ret= str[:37]
    except:
        pass    
    return ret
   
def doLogin(username, password):
  headers2 = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Accept-Language': 'en-US,en;q=0.5'
  }
  
  req = urllib2.Request(urllib2.unquote("https://www.fshare.vn/login"),headers=headers2)
  f = urllib2.urlopen(req)
  cookie = f.headers.get('Set-Cookie')
  
  soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
  results=soup.find('input', {'name': 'fs_csrf'})

  form_fields = {"LoginForm[email]": username
                 ,"LoginForm[password]": password
                 ,"LoginForm[rememberMe]":"0"
                 ,'fs_csrf':results['value']
                 ,'yt0':'Dang nhap'
                }
  
  headers['Cookie'] = cookie  
  form_data = urllib.urlencode(form_fields)
  response = urlfetch.fetch(
    url = 'https://www.fshare.vn/login',
    method='POST',
    headers = headers,
    data=form_data,
    follow_redirects = False)
  
  cookie = response.headers.get('set-cookie', '')
  hdr = response.headers  


  if (response.content==None) or (response.content==""):      
      print("Dang nhap thanh cong")
  else:
      cookie=None
      print("Dang nhap khong thanh cong")
  #new
  #urlfetch.get("https://www.fshare.vn/logout",headers=hdr, follow_redirects=False)
  '''
  req = urllib2.Request(urllib2.unquote("https://www.fshare.vn/logout"),headers=headers2)
  f = urllib2.urlopen(req)   
  print(BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES))
  '''
  return cookie
  
def createRq(url, url2, ck):
        '''
        req = urllib2.Request(urllib2.unquote("https://www.fshare.vn/home"))
        req.add_header('cookie', ck)
        f = urllib2.urlopen(req)
        soup = BeautifulSoup(f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
        '''
        cktemp = "__utma=54639420.686624083.1417677365.1417750147.1417758107.5; __utmz=54639420.1417677365.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); "+getSessionId(ck)+"; advertising_popup=closed; __utmc=54639420"
        
        headers2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection':'keep-alive',
            'Cookie': cktemp
        }

        headers3 = {
            'Cookie': ck
        }
        try: 
            req = urllib2.Request(urllib2.unquote(url),headers=headers2)
            f = urllib2.urlopen(req)
            cookie = f.headers.get('Set-Cookie')   
            req2 = urllib2.Request(urllib2.unquote(url2),headers=headers2)
            #req2.add_header('cookie', cookie)
            f2 = urllib2.urlopen(req2)
            body=f2.read()
            return body
        except urllib2.URLError, e:
            print 'We failed to open "%s".' % url
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code

def addLink(date, name, duration, href, thumb, desc, ck):
        print("tai day:")
        print(href)
        #soup1 = BeautifulSoup(createRq(href,"https://www.fshare.vn/download/index", ck), convertEntities=BeautifulSoup.HTML_ENTITIES)        
        #href = soup1.getString()
        description = date+'\n\n'+desc
        u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&mode=4"
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration})
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def addDir(name,url,mode,iconimage,query='',type='folder',page=0):        
        u = build_url({'url':urllib.quote_plus(url),'mode': str(mode), 'query': str(query), 'type':str(type), 'page':str(page)})
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
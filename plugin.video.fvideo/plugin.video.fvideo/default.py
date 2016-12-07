import CommonFunctions as common
import urllib
import urllib2
import urlparse
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import StorageServer
import urlfetch
import Cookie
import xbmc
import sys
import xutils
import google
import top250
import vaphim
from BeautifulSoup import BeautifulSoup
try:
    import json
except:
    import simplejson as json
import xfshare

__settings__ = xbmcaddon.Addon(id='plugin.video.fvideo')
#__settings__ = xbmcaddon.Addon(id='plugin.video.developing')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
cache = StorageServer.StorageServer("fshare_0")
searchnum = __settings__.getSetting('search_num')
activeDownload = __settings__.getSetting('activedowload')
sharinglist = __settings__.getSetting('sharinglist')

HTTP_DESKTOP_UA = {
    'Host':'www.fshare.vn',
    'Accept-Encoding':'gzip, deflate',
    'Referer':'https://www.fshare.vn/login.php',
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
}
headers=HTTP_DESKTOP_UA
SEARCH_URL='http://www.google.com/custom?hl=en&q=site:fshare.vn/%s+%s&num=%s&start=%s&as_qdr=%s'
FSLINK='http://fslink.us'
searchList=[]

ck = xutils.doLogin(__settings__.getSetting('username'),__settings__.getSetting('password'))
#ck = xutils.doLogin("abc","def")
#ck = ""

def resolve_url(url):
    if(activeDownload=="1"):
        headers['Cookie'] = ck
        response = urlfetch.get(url,headers=headers, follow_redirects=False)
        url=response.headers['location']
    else:
        soup1 = BeautifulSoup(xutils.createRq(url,"https://www.fshare.vn/download/index", ck), convertEntities=BeautifulSoup.HTML_ENTITIES)        
        url = soup1.getString()    
    item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def mainMenu():
    if (ck<>None) and (ck<>""):
        xutils.addDir('Tim kiem (Google)', '', 'gSearch', icon, '', '', 0)
        xutils.addDir('Tim kiem (VaPhim)', '', 'vSearch', icon, '', '', 0)
        xutils.addDir('Xem theo ID (cho ca Folder va File, vi du: KIMSN1RFJ7)', '', 'filmId', icon, '', '', 0)
        #xutils.addDir('Top 250', "http://akas.imdb.com/chart/top", 'top250', icon)
        xutils.addDir("Top 250", "http://vaphim.com/2011/11/14/imdb-top-250-films-cap-nhat-hang-ngay/", 'vaphimLazy', "http://vaphim.com/wp-content/uploads/2012/01/PBN.jpg?240a33", '', '', 0)
        xutils.addDir('V - phim le', "", 'vaphimMenu', icon)
        xutils.addDir('V - phim bo', "", 'vaphimBo', icon)
        xutils.addDir('V - ca nhac', "", 'vaphimCanhac', icon)
        xutils.addDir('V - suu tap', "http://vaphim.com/category/collection/", 'vaphimList', icon)
        xutils.addDir('Chia se cho nhau', "", 'sharingTogether', icon)
        xutils.addDir('Thu link', "", 'testLink', icon)
        xutils.addDir('Cau hinh FVideo', "", 'config', icon)
        #(name,url,mode,iconimage,query='',type='folder',page=0):
    else:
        xbmc.executebuiltin("xbmc.Notification('FVideo - message','Login failed')")
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('FVideo - message', 'Login failed (Please check: network or username or password)')
    
def sharingTogether():
    list = sharinglist.split(",")
    for item in list:
        name = item.strip()
        xutils.addDir(name, name, 'getFromfile', icon)
    
    #xutils.addDir('Phim hanh dong', "hanhdong.fvideo", 'getFromfile', icon)
    #xutils.addDir('Dac biet', "dacbiet.fvideo", 'getFromfile', icon)
    
def testLink():    
    xutils.addLink('', "Bau troi mau", 0, 'https://www.fshare.vn/file/KIMSN1RFJ7', '', 'Desc ...',ck)
    xutils.addLink('', "Loi nguyen bong ma", 0, 'https://www.fshare.vn/file/I7N2ABASHN', '', 'Desc ...',ck)
    xutils.addLink('', "Tho san", 0, 'https://www.fshare.vn/file/41X3N8SC2Q', '', 'Desc ...',ck)
    xutils.addLink('', "Truy tim bi an", 0, 'https://www.fshare.vn/file/0TO90XAXMO', '', 'Desc ...',ck)

def vaphimCanhac():
    xutils.addDir("Tuyen tap Thuy nga", "http://vaphim.com/2012/01/18/paris-by-night-collections/", 'vaphimLazy', "http://vaphim.com/wp-content/uploads/2012/01/PBN.jpg?240a33", '', '', 0)
    xutils.addDir("Tuyen tap Asia", "http://vaphim.com/2012/08/17/18243/", 'vaphimLazy', "http://vaphim.com/wp-content/uploads/2012/08/asia.jpg?240a33", '', '', 0)
    xutils.addDir("Tuyen tap Van son", "http://vaphim.com/2012/03/05/bo-suu-tap-dvd-van-son-collection/", 'vaphimLazy', "http://vaphim.com/wp-content/uploads/2012/03/Van-Son-Collection.jpg?240a33", '', '', 0)

def vaphimBo():
    xutils.addDir('Phim bo My', "http://vaphim.com/category/phim-2/series/us-tv-series/", 'vaphimList', icon)
    xutils.addDir('Phim bo Hong Kong', "http://vaphim.com/category/phim-2/series/hongkong-series/", 'vaphimList', icon)
    xutils.addDir('Phim bo Han', "http://vaphim.com/category/phim-2/series/korean-series/", 'vaphimList', icon)    
        
def vaphimMenu():
    xutils.addDir('Thuyet minh', "http://vaphim.com/category/phim-2/thuyet-minh-tieng-viet/", 'vaphimList', icon)
    xutils.addDir('Thieu nhi', "http://vaphim.com/category/phim-2/family/", 'vaphimList', icon)
    xutils.addDir('Hoat hinh', "http://vaphim.com/category/phim-2/animation/", 'vaphimList', icon)    
    xutils.addDir('Hanh dong', "http://vaphim.com/category/phim-2/action/", 'vaphimList', icon)
    xutils.addDir('Hinh su', "http://vaphim.com/category/phim-2/crime/", 'vaphimList', icon)
    xutils.addDir('Rung ron', "http://vaphim.com/category/phim-2/thriller/", 'vaphimList', icon)
    xutils.addDir('Lich su', "http://vaphim.com/category/phim-2/history/", 'vaphimList', icon)
    xutils.addDir('Phieu luu', "http://vaphim.com/category/phim-2/adventure/", 'vaphimList', icon)
    xutils.addDir('Than thoai', "http://vaphim.com/category/phim-2/fantasy/", 'vaphimList', icon)    
    xutils.addDir('Huyen bi', "http://vaphim.com/category/phim-2/mystery/", 'vaphimList', icon)
    xutils.addDir('Vien tuong', "http://vaphim.com/category/phim-2/sci-fi/", 'vaphimList', icon)
    xutils.addDir('Cao boi', "http://vaphim.com/category/phim-2/western/", 'vaphimList', icon)
    xutils.addDir('Chien tranh', "http://vaphim.com/category/phim-2/war/", 'vaphimList', icon)
    xutils.addDir('Tam ly', "http://vaphim.com/category/phim-2/drama/", 'vaphimList', icon)
    xutils.addDir('Lang man', "http://vaphim.com/category/phim-2/romance/", 'vaphimList', icon)
    xutils.addDir('Phim 18+', "http://vaphim.com/category/phim-2/18/", 'vaphimList', icon)
    
def lazyLink():
    xutils.addLink('', query, 0, urllib2.unquote(url), '', 'Desc ...',ck)
            
def search(sinput):
    if sinput is None or sinput=='':
        sinput=common.getUserInput('Google searching', '')
    elements = google.search('', sinput, '', page,searchnum)
    data = json.loads(elements)
    for ff in data["files"]:
        try:
            xutils.addLink('', ff["name"], 0, ff["href"], '', '',ck)
        except:
            pass        
    for ff in data["folders"]:
        try:
            xutils.addDir("["+ff["name"].encode("utf-8")+"]", ff["href"], 'fshareFolder', icon,ff["name"].encode("utf-8"))
        except:
            pass 
        #(name,url,mode,iconimage,query='',type='folder',page=0):
        #xutils.addDir(fo["name"], fo["href"], 'fForder', icon, sinput, '',page)
    snext = data["next"]

    if snext=='1':
        xutils.addDir('Next >', '', 'gSearch', icon, sinput, '', page+1)

def vaphimSearching():
    sinput=common.getUserInput('Vaphim searching', '')
    if(sinput<>None) and (sinput<>""):
        vaphimList(sinput)
        
def imdbAll():
    elements = top250.getAll('')
    data = json.loads(elements)
    for ff in data["items"]:
        try:
            keyword = ff["name"]
            if len(ff["name"])>11:
                keyword=ff["name"][0:8]
            xutils.addDir(ff["name"], '', 'gSearch', ff["icon"], keyword, '', 0)
        except:
            pass
        
def vaphimList(sinput):
    if(sinput==""):
        elements = vaphim.getAll(url)
    else:
        elements = vaphim.searching(sinput)
        
    data = json.loads(elements)
    for ff in data["items"]:
        try:
            xutils.addDir(ff["name"].encode("utf-8"), ff["href"], 'vaphimDetail', ff["icon"], '', '', 0)
        except:
            pass
    if data["next"] <>"":
        xutils.addDir("Next >", data["next"], 'vaphimList', icon, '', '', 0)

def vaphimDetail(strType):    
    elements = vaphim.getLink(url)
    data = json.loads(elements)
    if strType == "lazyLink":
        for ff in data["files"]:
            try:
                xutils.addDir(ff["name"].encode("utf-8"), ff["href"], 'lazyLink', icon,ff["name"].encode("utf-8"))
            except:
                pass
    else:
        for ff in data["files"]:
            try:
                xutils.addDir(ff["name"].encode("utf-8"), ff["href"], 'lazyLink', icon,ff["name"].encode("utf-8"))
                #xutils.addLink('', ff["name"].encode("utf-8"), 0, ff["href"], '', 'Desc ...',ck)
            except:
                pass
    for ff in data["folders"]:
        try:
            xutils.addDir("["+ff["name"].encode("utf-8")+"]", ff["href"], 'fshareFolder', icon,ff["name"].encode("utf-8"))
            #xutils.addLink('', ff["name"].encode("utf-8"), 0, ff["href"], '', 'Desc ...',ck)
        except:
            pass                

def fshareGetFileFromFolder(strType):    
    elements = xfshare.getFileFromFolder(url)
    data = json.loads(elements)
    if strType == "lazyLink":
        for ff in data["files"]:
            try:
                xutils.addDir(ff["name"].encode("utf-8"), ff["href"], 'lazyLink', icon,ff["name"].encode("utf-8"))
            except:
                pass
        for ff in data["folders"]:
            try:
                xutils.addDir("["+ff["name"].encode("utf-8")+"]", ff["href"], 'fshareFolder', '','')
            except:
                pass            
            
    else:
        for ff in data["files"]:
            try:
                xutils.addDir(ff["name"].encode("utf-8"), ff["href"], 'lazyLink', icon,ff["name"].encode("utf-8"))
                #xutils.addLink('', ff["name"].encode("utf-8"), 0, ff["href"], '', 'Desc ...',ck)
            except:
                pass
        for ff in data["folders"]:
            try:
                xutils.addDir("["+ff["name"].encode("utf-8")+"]", ff["href"], 'fshareFolder', '','')
            except:
                pass
                                    
def filmId():
    sinput=common.getUserInput('Film ID', '')
    hrefFile = 'https://www.fshare.vn/file/'+sinput
    hrefFolder = 'https://www.fshare.vn/folder/'+sinput
    xutils.addLink('', "File: " + sinput, 0, hrefFile, '', '',ck)
    xutils.addDir("["+sinput+"]", hrefFolder, 'fshareFolder', icon,sinput)

def getFromfile():
    try:
        file = open(xbmc.translatePath( __settings__.getAddonInfo('profile') ) + url,'r')
        #file = open(url,'r')
        for line in file.readlines():
            try:        
                list = line.split("##")
                href = list[1].strip()
                name = list[0].encode("utf-8")
                if href.find('fshare.vn/file')>0:
                    xutils.addDir(name,href , 'lazyLink', icon,name)
                elif href.find('fshare.vn/folder')>0:
                    xutils.addDir("["+name+"]", href, 'fshareFolder', icon,name)
            except:
                pass
        file.close()
    except:               
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('FVideo - message', 'Data not found')
        pass 
        
        
xbmcplugin.setContent(int(sys.argv[1]), 'movies')
url=''
mode=None
query=''
page=0
if sys.argv[2] is None:
    sys.argv[2]=''
if sys.argv[2]<>'':
    args = urlparse.parse_qs(sys.argv[2].replace('?',''))
    try:
        page = int(args.get('page')[0])
    except:
        pass       
    try:
        query=args.get('query')[0]
    except:
        pass
    try:
        mode = args.get('mode')[0]
    except:
        pass
    try:
        url = args.get('url')[0]
    except:
        pass

if mode==None:
	mainMenu()
elif mode=='4':
    resolve_url(url)
elif mode=='gSearch':
    search(query)
elif mode=='top250':
    imdbAll()
elif mode=='testLink':
    testLink()
elif mode=='filmId':
    filmId()
elif mode=='vaphimList':
    vaphimList("")
elif mode=='vaphimMenu':
    vaphimMenu()
elif mode=='vaphimBo':
    vaphimBo()
elif mode=='vaphimDetail':
    vaphimDetail("")
elif mode=='vaphimCanhac':
    vaphimCanhac()
elif mode=='vaphimLazy':
    vaphimDetail("lazyLink")
elif mode=='vSearch':
    vaphimSearching()
elif mode=='lazyLink':
    lazyLink()
elif mode=='fshareFolder':
    fshareGetFileFromFolder("lazyLink")
elif mode=='sharingTogether':
    sharingTogether()
elif mode=='getFromfile':
    getFromfile()
elif mode=='config':
   __settings__.openSettings()
                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
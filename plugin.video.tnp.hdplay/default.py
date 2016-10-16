#!/usr/bin/python
#coding=utf-8

import urllib, urllib2, os, re, zipfile
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.tnp.hdplay')
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
msicon = xbmc.translatePath(os.path.join(home, 'mediashare.png'))

baseurl = 'https://raw.githubusercontent.com/thanh51/repository.thanh51/master/PlaylistHDplay.xml'

# If not exist, install repository.thanhnguyenphu
try:
	ReposFolder = xbmc.translatePath('special://home/addons')
	if not os.path.isdir(os.path.join(ReposFolder, 'repository.thanhnguyenphu')):
		zip = zipfile.ZipFile(os.path.join(home, 'repository.thanhnguyenphu.zip'), 'r')
		zip.extractall(ReposFolder)
		zip.close()
except:
	pass

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link
	except:
		pass

def get_categories():
	add_dir('[COLOR yellow][B]Go to [COLOR blue][B]MediaShare[/B][/COLOR]', 'plugin://plugin.video.tnp.mediashare', None, msicon, fanart)
	content = make_request(baseurl)
	content = ''.join(content.splitlines()).replace('\t', '')
	match = re.compile('<item>(.+?)</item>').findall(content)
	for item in match:
		title = ""
		link = ""
		thumb = ""
		if '<title>' in item:
			title = re.compile('<title>(.+?)</title>').findall(item)[0].strip()
		if '<link>' in item:
			link = re.compile('<link>(.*?)</link>').findall(item)[0].replace('&amp;', '&').strip()
		if '<thumbnail>' in item:
			thumb = re.compile('<thumbnail>(.*?)</thumbnail>').findall(item)[0].strip()
		add_link(title, link, '%s/%s.png'%(xbmc.translatePath('special://home/addons/plugin.video.tnp.hdplay'), thumb), fanart)

def resolve_url(url):
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def add_dir(name, url, mode, iconimage, fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", fanart)
	if "plugin.video.tnp" in url:
		u = url
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def add_link(name, url, iconimage, fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=1"+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", fanart)
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
	return param

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=''
name=None
mode=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:pass

if mode==None: get_categories()
elif mode==1: resolve_url(url)
 
xbmcplugin.endOfDirectory(int(sys.argv[1]))
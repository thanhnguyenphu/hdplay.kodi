#!/usr/bin/python
#coding=utf-8

import os, re, urllib, urllib2, shutil
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

addon = xbmcaddon.Addon(id='plugin.video.tnp.hdplay')
addon_version = addon.getAddonInfo('version')

kodiVersion = int(xbmc.getInfoLabel("System.BuildVersion")[:2])
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
icon = os.path.join(home, 'icon.png')
fanart = os.path.join(home, 'fanart.jpg')
thumbnails = os.path.join(home, 'resources', 'thumbnails')
settings_icon = os.path.join(thumbnails, 'settings.png')
ms_icon = os.path.join(thumbnails, 'mediashare.png')

url_1 = 'https://raw.githubusercontent.com/thanh51/repository.thanh51/master/PlaylistHDplay.m3u'

url_2 = 'http://textuploader.com/d544e/raw'

subtitle = 'https://raw.githubusercontent.com/thanh51/repository.thanh51/master/mungnammoi.srt'

# If not exist, install repository.thanhnguyenphu
# Nếu chưa có, cài repository.thanhnguyenphu
try:
	ReposFolder = xbmc.translatePath('special://home/addons')
	if not os.path.isdir(os.path.join(ReposFolder, 'repository.thanhnguyenphu')):
		import zipfile
		thanh_repo = 'https://github.com/thanhnguyenphu/hdplay.kodi/raw/master/zips/repository.thanhnguyenphu/repository.thanhnguyenphu-1.0.0.zip'
		thanhrepo = os.path.join(ReposFolder, 'packages', 'thanhrepo.zip')
		urllib.urlretrieve(thanh_repo, thanhrepo)
		zip = zipfile.ZipFile(thanhrepo, 'r')
		zip.extractall(ReposFolder)
		zip.close()
		os.remove(thanhrepo)
		if kodiVersion > 16:
			from sqlite3 import dbapi2 as db_lib
			set_it = 1
			db_path = xbmc.translatePath(os.path.join('special://profile', 'Database', 'Addons27.db'))
			conn = db_lib.connect(db_path)
			conn.execute('REPLACE INTO installed (addonID,enabled) VALUES(?,?)', ('repository.thanhnguyenphu' ,set_it, ))
			conn.commit()
except:
	pass

def addon_log(string):
	if kodiVersion < 17:
		xbmc.log("[plugin.video.tnp.hdplay-%s]: %s" % (addon_version, string))
	else:
		xbmc.log("[plugin.video.tnp.hdplay-%s]: %s" % (addon_version, string), xbmc.LOGNOTICE)

def make_request(url, headers=None):
	if headers is None:
			headers  = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
						'Referer' : 'http://www.google.com'}
	try:
			req = urllib2.Request(url,headers=headers)
			response = urllib2.urlopen(req)
			content = response.read()
			response.close()
			return content
	except urllib2.URLError, e:
		addon_log('URL: '+url)
		if hasattr(e, 'code'):
			addon_log('We failed with error code - %s.' % e.code)
			xbmc.executebuiltin("XBMC.Notification(HDPlay,We failed with error code - "+str(e.code)+",5000,"+icon+")")
		elif hasattr(e, 'reason'):
			addon_log('We failed to reach a server.')
			addon_log('Reason: %s' %e.reason)
			xbmc.executebuiltin("XBMC.Notification(HDPlay,We failed to reach a server. - "+str(e.reason)+",5000,"+icon+")")

def get_categories():

	add_dir('[COLOR yellow][B]Go to [/B][/COLOR][COLOR blue][B]MediaShare Add-on[/B][/COLOR]', 'plugin://plugin.video.tnp.mediashare', None, ms_icon, fanart)
	add_dir('[COLOR lime][B]Cài Đặt [/B][/COLOR][B]và [/B][COLOR cyan][B]Tự Động Xoá Cache[/B][/COLOR]', 'AddonSettings', 1, settings_icon, fanart)

	if urllib.urlopen(url_1).getcode() == 200:
		addon_log('URL: '+url_1)
		content = make_request(url_1)
	else:
		addon_log('URL: '+url_2)
		content = make_request(url_2)

	if '#EXTINF' in content:
		m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
		m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
		group_title_regex = 'group-title=[\'"](.*?)[\'"]'
		match = re.compile(m3u_regex).findall(content)
		for group_logo, title, link in match:
			if 'group-title' in group_logo:
				group = re.compile(group_title_regex).findall(str(group_logo))[0].strip()
				if len(group) > 0:
					group_title = ('%s%s%s'%('[COLOR blue][', group, '][/COLOR] '))
				else:
					group_title = ''
			else:
				group_title = ''
			if 'tvg-logo' in group_logo:
				thumb = re.compile(m3u_thumb_regex).findall(str(group_logo))[0].strip()
				if len(thumb) > 0:
					if thumb.startswith('http'):
						thumb = thumb.replace(' ', '%20')
					else:
						thumb = icon
				else:
					thumb = icon
			else:
				thumb = icon
			title = title.strip()
			link = link.strip()
			add_link(('%s%s'%(group_title, title)), link, thumb, fanart)

	else:
		content = ''.join(content.splitlines()).replace('\t', '')
		match = re.compile('<item>(.+?)</item>').findall(content)
		for item in match:
			title = ""
			link = ""
			thumb = ""
			if '<title>' in item:
				title = re.compile('<title>(.+?)</title>').findall(item)[0].strip()
			if '<link>' in item:
				link = re.compile('<link>(.*?)</link>').findall(item)[0].strip()
			if '<thumbnail>' in item:
				thumb = re.compile('<thumbnail>(.*?)</thumbnail>').findall(item)[0].strip()
			if len(thumb) > 0:
				if thumb.startswith('http'):
					thumb = thumb.replace(' ', '%20')
				else:
					thumb = icon
			else:
				thumb = icon
			add_link(title, link, thumb, fanart)

def addon_settings():
	clear_cache()
	addon.openSettings()
	sys.exit(0)

def clear_cache():  #### plugin.video.xbmchubmaintenance ####
	try:
		xbmc_cache_path = xbmc.translatePath('special://temp')
		if os.path.exists(xbmc_cache_path) == True:
			for root, dirs, files in os.walk(xbmc_cache_path):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					for f in files:
						try:
							os.unlink(os.path.join(root, f))
						except:
							pass
					for d in dirs:
						if any(x in d for x in ['subs', 'xshare', 'temp']):
							pass
						else:
							try:
								shutil.rmtree(os.path.join(root, d))
							except:
								pass
	except:
		pass

def resolve_url(url):
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	if len(subtitle) > 0:
		try:
			xbmc.sleep(3000)
			xbmc.Player().setSubtitles(subtitle)
		except:
			pass
	return

def add_dir(name, url, mode, iconimage, fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", fanart)
	if 'plugin' in url:
		u = url
	ok=xbmcplugin.addDirectoryItem(int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def add_link(name, url, iconimage, fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=2"
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	liz.setProperty("Fanart_Image", fanart)
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(int(sys.argv[1]),url=u,listitem=liz)
	return ok

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

params = get_params()

url = ''
name = None
mode = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass

if mode == None:
	get_categories()

elif mode == 1:
	addon_settings()

elif mode == 2:
	resolve_url(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

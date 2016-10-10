import CommonFunctions as common
import urllib
import urllib2
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import urlfetch
import re
import json
from BeautifulSoup import BeautifulSoup

__settings__ = xbmcaddon.Addon(id='plugin.video.tnp.hdplay')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
thumbnails = xbmc.translatePath( os.path.join( home, 'thumbnails\\' ) )

def _makeCookieHeader(cookie):
	cookieHeader = ""
	for value in cookie.values():
			cookieHeader += "%s=%s; " % (value.key, value.value)
	return cookieHeader

def make_request(url, headers=None):
	if headers is None:
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
								 'Referer' : 'http://www.google.com'}
	try:
			req = urllib2.Request(url,headers=headers)
			f = urllib2.urlopen(req)
			body=f.read()
			return body
	except urllib2.URLError, e:
			print 'We failed to open "%s".' % url
			if hasattr(e, 'reason'):
					print 'We failed to reach a server.'
					print 'Reason: ', e.reason
			if hasattr(e, 'code'):
					print 'We failed with error code - %s.' % e.code
#def get_fpt():
	add_link('', 'Fashion TV', 0, 'http://hlscache.fptplay.net.vn/sopchannel/fashiontv.stream/playlist.m3u8', '', '')
	add_link('', 'MTV', 0, 'http://hlscache.fptplay.net.vn/sopchannel/mtvviet.stream/playlist.m3u8', '', '')
	add_link('', 'Star World', 0, 'http://hlscache.fptplay.net.vn/sopchannel/starworld.stream/playlist.m3u8', '', '')
	add_link('', 'Cinemax', 0, 'http://hlscache.fptplay.net.vn/sopchannel/cinemax.stream/playlist.m3u8', '', '')
	add_link('', 'Discovery Channel', 0, 'http://hlscache.fptplay.net.vn/sopchannel/discoverychannel.stream/playlist.m3u8', '', '')
	add_link('', 'Channel V', 0, 'http://hlscache.fptplay.net.vn/sopchannel/channelv.stream/playlist.m3u8', '', '')
	add_link('', 'Cartoon Network', 0, 'http://hlscache.fptplay.net.vn/sopchannel/cartoonnetwork.stream/playlist.m3u8', '', '')
	add_link('', 'Animal Planet', 0, 'http://hlscache.fptplay.net.vn/sopchannel/animalplanet.stream/playlist.m3u8', '', '')
	add_link('', 'National Geographic', 0, 'http://hlscache.fptplay.net.vn/sopchannel/nationalgeographic.stream/playlist.m3u8', '', '')
	add_link('', 'National Geographic Adventure', 0, 'http://hlscache.fptplay.net.vn/sopchannel/nationalgeographicadventure.stream/playlist.m3u8', '', '')
	add_link('', 'Nation Geographic Wild', 0, 'http://hlscache.fptplay.net.vn/sopchannel/nationalgeographicwild.stream/playlist.m3u8', '', '')
	add_link('', 'True Visions', 0, 'http://hlscache.fptplay.net.vn/sopchannel/truevisions.stream/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 1', 0, 'http://hlscache.fptplay.net.vn/event/sport1/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 2', 0, 'http://hlscache.fptplay.net.vn/event/sport2/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 3', 0, 'http://hlscache.fptplay.net.vn/event/sport3/playlist.m3u8', '', '')
	add_link('', 'Net TV Sport 4', 0, 'http://hlscache.fptplay.net.vn/event/sport4/playlist.m3u8', '', '')
	add_link('', 'Star Sport', 0, 'http://hlscache.fptplay.net.vn/sopchannel/starsports.stream/playlist.m3u8', '', '')
	add_link('', 'FOX Sport', 0, 'http://hlscache.fptplay.net.vn/sopchannel/foxsports.stream/playlist.m3u8', '', '')

	content = make_request('http://play.fpt.vn/livetv/')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', {'class' : 'channel_link'})
	for item in items:
		img = item.find('img')
		if img is not None:
			try:
				add_link('', item['channel'], 0, 'http://play.fpt.vn' + item['href'], img['src'], '')
			except:
				pass
#add_dir(name,url,mode,iconimage,query='',type='f',page=0):
def get_vtc_movies(url, query='25', type='', page=0):
	if url == '':
		content = make_request('http://117.103.206.21:88/Movie/GetMovieGenres?device=4')
		result = json.loads(content)
		for item in result:
			add_dir(item["Name"], 'http://117.103.206.21:88/Movie/GetMoviesByGenre?device=4&genreid=' + str(item["ID"]) + '&start=0&length=25', 11, '', '25', str(item["ID"]), 0)
	if 'GetMoviesByGenre' in url:
		content = make_request(url)
		result = json.loads(content)
		for item in result:
			add_link('', item["Title"], 0, 'http://117.103.206.21:88/Movie/GetMovieStream?device=4&path=' + item["MovieUrls"][0]["Path"].replace('SD', 'HD'), item["Thumbnail3"], item["SummaryShort"])
		add_dir('Next', 'http://117.103.206.21:88/Movie/GetMoviesByGenre?device=4&genreid=' + type + '&start=' + str(int(query)+page) + '&length=' + str(query), 11, '', str(int(query)+page), type, page)
	
def get_vtc(url = None):
	content = make_request(url)
	
	result = json.loads(content)
	for item in result:
		path = item["ChannelUrls"][0]["Path"]
		if 'http' in path:
			add_link('', item["Name"], 0, item["ChannelUrls"][0]["Path"], item["Thumbnail2"], '')
		else:
			add_link('', item["Name"], 0, "http://117.103.206.21:88/channel/GetChannelStream?device=4&path=" + item["ChannelUrls"][0]["Path"], item["Thumbnail2"], '')

def get_hdonline(url = None):
	if url == '':
		content = make_request('http://hdonline.vn/')
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.find('div',{'id' : 'full-mn-phim-le'}).findAll('a')
		for item in items:
			href = item.get('href')
			if href is not None:
				try:
					add_dir(item.text, href, 13, thumbnails + 'HDOnline.png', query, type, 0)
				except:
					pass
		return
	if 'xem-phim' in url:	
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.findAll('ul', {'class' : 'clearfix listmovie'})[1].findAll('li')
		for item in items:
			a = item.find('a')
			img = item.find('img')
			span = item.find('span',{'class' : 'type'})
			href = a.get('href')
			if href is not None:
				try:
					if span is not None:
						add_dir(a.get('title') + ' (' + span.text + ')', href, 9, a.img['src'], '', '', 0)
					else:	
						add_link('', a.get('title'), 0, href, img['src'], '')
				except:
					pass
		items = soup.find('div',{'class' : 'pagination pagination-right'})
		if items is not None:
			for item in items.findAll('a'):
				a = item
				href = a.get('href')
				if href is not None:
					try:
						add_dir(a.get('title'), href, 9, thumbnails + 'zui.png', '', '', 0)
					except:
						pass
		
def get_zui(url = None):
	if url == '':
		content = make_request('http://zui.vn')
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		items = soup.find('div',{'class' : 'span8 visible-desktop visible-tablet'}).findAll('a')
		for item in items:
			href = item.get('href')
			if href is not None:
				try:
					add_dir(item.text, href, 9, thumbnails + 'zui.png', query, type, 0)
				except:
					pass
		return
	if 'the-loai' in url or 'phim-' in url:	
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		groups = soup.find('ul', {'class' : 'group'})
		if groups is not None:
			for item in groups.findAll('a'):
				matchObj = re.match( r'change_group_chapter\((\d+),(\d+),(\d+)\)', item['onclick'], re.M|re.I)
				response = urlfetch.fetch(
			url = 'http://zui.vn/?site=movie&view=show_group_chapter',
			method ='POST',
			data = {
				"pos": matchObj.group(1),
				"movie_id": matchObj.group(2),
				"type": matchObj.group(3)
			}
		)
				soup = BeautifulSoup(str(response.content), convertEntities=BeautifulSoup.HTML_ENTITIES)
				for item in soup.findAll('a'):
					add_link('', u'Tập ' + item.text, 0, 'http://zui.vn/' + item['href'], thumbnails + 'zui.png', '')
		else:
			items = soup.find('ul',{'class' : 'movie_chapter'})
			if items is not None:
				for item in items.findAll('a'):
					a = item
					href = a.get('href')
					if href is not None:
						try:
							add_link('', u'Tập ' + a.text, 0, 'http://zui.vn/' + href, thumbnails + 'zui.png', '')
							#add_dir(u'Tập ' + a.text, 'http://zui.vn/' + href, 9, thumbnails + 'zui.png', '', '', 0)
						except:
							pass
			else:
				items = soup.findAll('div',{'class' : 'poster'})
				for item in items:
					a = item.find('a')
					span = item.find('span',{'class' : 'type'})
					href = a.get('href')
					if href is not None:
						try:
							if span is not None:
								add_dir(a.get('title') + ' (' + span.text + ')', href, 9, a.img['src'], '', '', 0)
							else:	
								add_link('', a.get('title'), 0, href, a.img['src'], '')
						except:
							pass
				items = soup.find('div',{'class' : 'pagination pagination-right'})
				if items is not None:
					for item in items.findAll('a'):
						a = item
						href = a.get('href')
						if href is not None:
							try:
								add_dir(a.get('title'), href, 9, thumbnails + 'zui.png', '', '', 0)
							except:
								pass
	else:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		groups = soup.find('ul', {'class' : 'group'})
		if groups is not None:
			for item in groups.findAll('a'):
				matchObj = re.match( r'change_group_chapter\((\d+),(\d+),(\d+)\)', item['onclick'], re.M|re.I)
				response = urlfetch.fetch(
			url = 'http://zui.vn/?site=movie&view=show_group_chapter',
			method ='POST',
			data = {
				"pos": matchObj.group(1),
				"movie_id": matchObj.group(2),
				"type": matchObj.group(3)
			}
		)
				soup = BeautifulSoup(str(response.content), convertEntities=BeautifulSoup.HTML_ENTITIES)
				for item in soup.findAll('a'):
					add_link('', u'Tập ' + item.text, 0, 'http://zui.vn/' + item['href'], thumbnails + 'zui.png', '')
			return
	
		items = soup.find('ul',{'class' : 'movie_chapter'})
		if items is not None:
			for item in items.findAll('a'):
				a = item
				href = a.get('href')
				if href is not None:
					try:
						add_link('', u'Tập ' + a.text, 0, 'http://zui.vn/' + href, thumbnails + 'zui.png', '')
						#add_dir(u'Tập ' + a.text, 'http://zui.vn/' + href, 9, thumbnails + 'zui.png', '', '', 0)
					except:
						pass
	
def get_fpt_other(url):
	content = make_request(url)
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a')
	for item in items:
		href = item.get('href')
		if href is not None and 'the-loai-more' in href and 'Xem' not in item.text:
			try:
				add_dir(item.text, 'http://play.fpt.vn' + href, 8, thumbnails + 'fptplay.jpg', query, type, 0)
			except:
				pass

def get_fpt_tvshow_cat(url):
	content = make_request(url)
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	if url is not None and '/Video/' not in url:
		items = soup.findAll('div', {'class' : 'col'})
		for item in items:
			img = item.a.img['src']
			href = item.a['href']
			text = item.a.img['alt']	
			try:
				add_dir(text, 'http://play.fpt.vn' + href, 8, img, '', '', 0)
			except:
				pass

	items = soup.find('ul', {'class' : 'pagination pagination-sm'}).findAll('a')
	for item in items:
		href = ''
		href = item.get('href')
		if href is not None and 'the-loai-more' in href and 'Xem' not in item.text:
			try:
				add_dir('Trang ' + item.text, 'http://play.fpt.vn' + href, 8, thumbnails + 'fptplay.jpg', query, type, 0)
			except:
				pass
		if href is not None and '/Video/' in href:
			try:
				add_link('', u'Tập ' + item.text, 0, 'http://play.fpt.vn' + href, thumbnails + 'fptplay.jpg', '')
			except:
				pass
		
def get_htv():
	content = make_request('http://www.htvonline.com.vn/livetv')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a', {'class' : 'mh-grids5-img'})
	for item in items:
		img = item.find('img')
		if img is not None:
			try:
				add_link('', item['title'], 0, item['href'], img['src'], '')
			except:
				pass

#def get_sctv(url):
	content = make_request('http://tv24.vn/LiveTV/Tivi_Truc_Tuyen_SCTV_VTV_HTV_THVL_HBO_STARMOVIES_VTC_VOV_BongDa_Thethao_Hai_ThoiTrang_Phim_PhimHongKong.html')
	soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
	items = soup.findAll('a')
	for item in items:
		img = item.find('img')
		if img is not None and 'LiveTV' in item['href']:
			try:
				add_link('', item['href'], 0, 'http://tv24.vn' + item['href'], img['src'], '')
			except:
				pass
		
def get_categories():

	add_link('', '[COLOR red][B]********** Chung Cho Các Mạng Internet *********[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', '[COLOR cyan][B]I - Kênh TV Cần addon f4mTester(thuộc repo Shani 2.9)[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'K+1 HD s1', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8546.ts', thumbnails + '', '')
	add_link('', 'K+1 HD s2', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://playlist.bulldogstreams.football:8000/live/jukka/jukka/8546.ts', thumbnails + '', '')
	add_link('', 'K+1 HD s3', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://89.163.148.31:8000/live/stakenborg/stakenborg/8546.ts', thumbnails + '', '')
	add_link('', 'K+1 HD s4', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://5.39.70.216/live/louis/louis/1031.ts', thumbnails + '', '')
	add_link('', 'K+PM HD s1', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8544.ts', thumbnails + '', '')
	add_link('', 'K+PM HD s2', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://playlist.bulldogstreams.football:8000/live/jukka/jukka/8544.ts', thumbnails + '', '')
	add_link('', 'K+PM HD s3', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://89.163.148.31:8000/live/stakenborg/stakenborg/8544.ts', thumbnails + '', '')
	add_link('', 'K+PM HD s4', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://5.39.70.216/live/louis/louis/1029.ts', thumbnails + '', '')
	add_link('', 'K+PC HD s1', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8545.ts', thumbnails + '', '')
	add_link('', 'K+PC HD s2', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://playlist.bulldogstreams.football:8000/live/jukka/jukka/8545.ts', thumbnails + '', '')
	add_link('', 'K+PC HD s3', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://89.163.148.31:8000/live/stakenborg/stakenborg/8545.ts', thumbnails + '', '')
	add_link('', 'K+PC HD s4', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://5.39.70.216/live/louis/louis/1030.ts', thumbnails + '', '')
	add_link('', 'Mio 102 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8537.ts', thumbnails + '', '')
	add_link('', 'Mio 103 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8538.ts', thumbnails + '', '')
	add_link('', 'Mio 104 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8539.ts', thumbnails + '', '')
	add_link('', 'Mio 105 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8540.ts', thumbnails + '', '')
	add_link('', 'Mio 106 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8541.ts', thumbnails + '', '')
	add_link('', 'Mio 107 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8542.ts', thumbnails + '', '')
	add_link('', 'Mio 108 HD', 0, 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=http://cp.dmbshare.net:8000/live/melih/melih/8543.ts', thumbnails + '', '')
		
	add_link('', '[COLOR cyan][B]II - Kênh sopcast (KODI đã cài addon Plexus)[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', '[COLOR=yellow][B]-> Lịch thi đấu: Web http://arenavision.in/agenda[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', '[COLOR=yellow][B]-> Xem Thi Đấu Theo Giờ VN + 5 Tiếng [/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', '[COLOR=yellow][B]-> K+ (Server VN) Có Thể Phát Vào các Ngày Cuối Tuần [/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'K+(253096) - Server VN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/253096&mode=2&name=K+(253096)', thumbnails + '', '') 
	add_link('', 'K+(259091) - Server VN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/259091&mode=2&name=K+(259091)', thumbnails + '', '') 
	add_link('', 'K+(259400) - Server VN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/259400&mode=2&name=K+(259400)', thumbnails + '', '') 
	add_link('', 'S1(262490) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262490&mode=2&name=S1(262490)', thumbnails + '', '') 
	add_link('', 'S2(262491) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262491&mode=2&name=S2(262491)', thumbnails + '', '') 
	add_link('', 'S3(262492) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262492&mode=2&name=S3(262492)', thumbnails + '', '') 
	add_link('', 'S4(262493) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262493&mode=2&name=S4(262493)', thumbnails + '', '') 
	add_link('', 'S5(262494) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262494&mode=2&name=S5(262494)', thumbnails + '', '') 
	add_link('', 'S6(262495) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262495&mode=2&name=S6(262495)', thumbnails + '', '') 
	add_link('', 'S7(262496) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262496&mode=2&name=S7(262496)', thumbnails + '', '')  
	add_link('', 'S8(262497) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262497&mode=2&name=S8(262497)', thumbnails + '', '') 
	add_link('', 'S9(262498) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262498&mode=2&name=S9(262498)', thumbnails + '', '')   
	add_link('', 'S10(262499) - Server NN', 0, 'plugin://program.plexus/?url=sop://broker.sopcast.com:3912/262499&mode=2&name=S10(262499)', thumbnails + '', '')

	add_link('', '[COLOR cyan][B]III - Kênh Thể Thao khác[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'SUPERSPORTS', 0, 'http://46.105.161.243:8085/lighd', thumbnails + '', '')
	add_link('', 'CCTV5 HD', 0, 'http://183.207.255.190:80/live/program/live/hdnba5/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'CCTV5+HD', 0, 'http://180.100.1.250/cdn/iptv/Tvod/001/ch00000090990000001043/index.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 1-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba1/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 2-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba2/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 3-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba3/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 4-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba4/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 5-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba5/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 6-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba6/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 7-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba7/4000000/mnf.m3u8', thumbnails + '', '')
	add_link('', 'China:Live 8-1080P', 0, 'http://183.207.255.190:80/live/program/live/hdnba8/4000000/mnf.m3u8', thumbnails + '', '') 
		
	add_link('', '[COLOR red][B]********* Chỉ Cho Mạng FPT **********[/B][/COLOR]', 0, '', thumbnails + '', '')
	add_link('', 'VTV1 HD', 0, 'http://118.69.252.4/tv/vtv1HD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV3 HD', 0, 'http://118.69.252.4/tv/vtv3HD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTV6 HD', 0, 'http://118.69.252.4/tv/vtv6HD/index.m3u8', thumbnails + '', '')
	add_link('', 'QPVN HD', 0, 'http://118.69.184.194/tv1/quocphongHD/index.m3u8', thumbnails + '', '')
	add_link('', 'THETHAOTV HD', 0, 'http://118.69.252.4/tv1/thethaoTVHD/index.m3u8', thumbnails + '', '')
	add_link('', 'BONGDATV HD', 0, 'http://118.69.252.4/tv1/bongdaTVHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV2 HD', 0, 'http://118.69.252.4/tv/htv2HD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV7 HD', 0, 'http://118.69.252.4/tv/htv7HD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTV9 HD', 0, 'http://118.69.252.4/tv/htv9HD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC MOVIE HD', 0, 'http://118.69.252.4/tv1/htvcmovieHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HTVC THUANVIET HD', 0, 'http://118.69.252.4/tv1/htvcthuanvietHD/index.m3u8', thumbnails + '', '')
	add_link('', 'VTC3 HD', 0, 'http://118.69.252.4/tv1/vtc3HD/index.m3u8', thumbnails + '', '')
	add_link('', 'ITV HD', 0, 'http://118.69.184.194/tv1/itvHD/index.m3u8', thumbnails + '', '')
	add_link('', 'STAR MOVIES HD', 0, 'http://118.69.252.4/tv3/StarMoviesHD/index.m3u8', thumbnails + '', '')
	add_link('', 'HBO HD', 0, 'http://118.69.252.4/tv3/HBOHD/index.m3u8', thumbnails + '', '')
	add_link('', 'AXN HD', 0, 'http://118.69.252.4/tv3/AXNHD/index.m3u8', thumbnails + '', '')
	add_link('', 'DISCOVERY WORLD HD', 0, 'http://118.69.252.4/tv3/DiscoveryWorldHD/index.m3u8', thumbnails + '', '')
	add_link('', 'NATIONAL GEOGRAPHIC HD', 0, 'http://118.69.252.4/tv3/NationalGeographicHD/index.m3u8', thumbnails + '', '')
	add_link('', 'CARTOON NETWORK HD', 0, 'http://118.69.252.4/tv3/CartoonNetworkHD/index.m3u8', thumbnails + '', '')
	add_link('', 'FASHION TV HD', 0, 'http://118.69.252.4/tv3/FashionTVHD/index.m3u8', thumbnails + '', '')
	add_link('', 'FOX SPORTS HD', 0, 'http://118.69.252.4/tv3/FoxSportsHD/index.m3u8', thumbnails + '', '')
	add_link('', 'CINEMAX', 0, 'http://118.69.252.4/tv3/Cinemax/index.m3u8', thumbnails + '', '')
	add_link('', 'DISCOVERY', 0, 'http://118.69.252.4/tv3/Discovery/index.m3u8', thumbnails + '', '')
	add_link('', 'ANIMAL PLANET', 0, 'http://118.69.252.4/tv3/AnimalPlanet/index.m3u8', thumbnails + '', '')
	add_link('', 'TLC', 0, 'http://118.69.252.4/tv3/TravelLiving/index.m3u8', thumbnails + '', '')
	add_link('', 'FOX SPORTS', 0, 'http://118.69.252.4/tv3/FoxSports/index.m3u8', thumbnails + '', '')
	add_link('', 'FOX SPORTS 2', 0, 'http://118.69.252.4/tv3/FoxSports2/index.m3u8', thumbnails + '', '')	
		
	#add_link('', 'HBO HD', 0, '', '', '')
	#http://scache.fptplay.net.vn/live/htvcplusHD_1000.stream/manifest.f4m
	#add_dir('HTVOnline', url, 5, thumbnails + 'htv.jpg', query, type, 0)
	#add_dir('SCTV', url, 12, thumbnails + 'SCTV.png', query, type, 0)
	#add_dir('VTCPlay - TV', 'http://117.103.206.21:88/Channel/GetChannels?device=4', 10, thumbnails + 'vtcplay.jpg', query, type, 0)
	#add_dir('VTCPlay - Movies', '', 11, thumbnails + 'vtcplay.jpg', query, type, 0)
	#add_dir('FPTPlay - TV', url, 6, thumbnails + 'fptplay_logo.jpg', query, type, 0)
	#add_dir('FPTPlay - TVShow', url, 7, thumbnails + 'fptplay_logo.jpg', query, type, 0)
	#add_dir('ZUI.VN', url, 9, thumbnails + 'zui.png', query, type, 0)
	#add_dir('HDOnline.vn', url, 13, thumbnails + 'HDOnline.png', query, type, 0)

def searchMenu(url, query = '', type='f', page=0):
	add_dir('New Search', url, 2, icon, query, type, 0)
	add_dir('Clear Search', url, 3, icon, query, type, 0)

	searchList=cache.get('searchList').split("\n")
	for item in searchList:
		add_dir(item, url, 2, icon, item, type, 0)

def resolve_url(url):
	if 'zui.vn' in url:
		headers2 = {'User-agent' : 'iOS / Chrome 32: Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/32.0.1700.20 Mobile/11B554a Safari/9537.53',
											 'Referer' : 'http://www.google.com'}
		content = make_request(url, headers2)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('movie_play_chapter'):
				#movie_play_chapter('mediaplayer', '1', 'rtmp://103.28.37.89:1935/vod3/mp4:/phimle/Vikingdom.2013.720p.WEB-DL.H264-PHD.mp4', '/uploads/movie_view/5c65563b1ce8d106c013.jpg', 'http://zui.vn/subtitle/Vikingdom.2013.720p.WEB-DL.H264-PHD.srt');
				matchObj = re.match( r'[^\']*\'([^\']*)\', \'([^\']*)\', \'([^\']*)\', \'([^\']*)\', \'([^\']*)\'', s, re.M|re.I)
				url = matchObj.group(3)
				url = url.replace(' ','%20')
				xbmc.Player().play(url)
				xbmc.Player().setSubtitles(matchObj.group(5))
				return
				break

	if 'play.fpt.vn/Video' in url:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('"<source src='):
				start = s.index('\'')+1
				end = s.index('\'', start+1)
				url = s[start:end]
				break

	if 'play.fpt.vn' in url:
		content = make_request(url)
		soup = BeautifulSoup(str(content), convertEntities=BeautifulSoup.HTML_ENTITIES)
		item = soup.find('div', {'id' : 'bitrate-tag'})
		url = item['highbitrate-link']
		content = make_request(url)
		for line in content.splitlines():
			s = line.strip()
			if s.startswith('<id>'):
				start = s.index('<id>')+4
				end = s.index('<', start+1)
				url = url.replace('manifest.f4m',s[start:end])
				url = 'http://scache.fptplay.net.vn/live/' + s[start:end] + '/playlist.m3u8'
				break

	if 'htvonline' in url:
		content = make_request(url)
		for line in content.splitlines():
			if line.strip().startswith('file: '):
				url = line.strip().replace('file: ', '').replace('"', '').replace(',', '')
				break

	#if 'tv24' in url:
		content = make_request(url)
		for line in content.splitlines():
			if line.strip().startswith('\'file\': \'http'):
				url = line.strip().replace('\'file\': ', '').replace('\'', '').replace(',', '')
				break
		
	if 'GetChannelStream' in url or 'GetMovieStream' in url or 'vtvplay' in url:
		content = make_request(url)
		url = content.replace("\"", "")
		url = url[:-5]
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def add_link(date, name, duration, href, thumb, desc):
	description = date+'\n\n'+desc
	u=sys.argv[0]+"?url="+urllib.quote_plus(href)+"&mode=4"
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Duration": duration})
	if 'zui' in href:
		liz.setProperty('IsPlayable', 'false')
	else:
		liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)



def add_dir(name,url,mode,iconimage,query='',type='f',page=0):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&query="+str(query)+"&type="+str(type)+"&page="+str(page)#+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()

url=''
name=None
mode=None
query=None
type='f'
page=0

try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
try:
	page=int(urllib.unquote_plus(params["page"]))
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "type: "+str(type)
print "page: "+str(page)
print "query: "+str(query)

if mode==None:
	get_categories()
#		fslink_get_video_categories(FSLINK+'/phim-anh.html')

elif mode==1:
	searchMenu(url, '', type, page)

elif mode==2:
	search(url, query, type, page)

elif mode==3:
	clearSearch()

elif mode==4:
	resolve_url(url)
elif mode==5:
	get_htv()
elif mode==6:
	get_fpt()
elif mode==7:
	get_fpt_other('http://play.fpt.vn/the-loai/tvshow')
	#get_fpt_other('http://play.fpt.vn/the-loai/sport')
	#get_fpt_other('http://play.fpt.vn/the-loai/music')
	#get_fpt_other('http://play.fpt.vn/the-loai/general')
elif mode==8:
	get_fpt_tvshow_cat(url)
elif mode==9:
	get_zui(url)
elif mode==10:
	get_vtc(url)
elif mode==11:
	get_vtc_movies(url, query, type, page)
#elif mode==12:
	get_sctv(url)
elif mode==13:
	get_hdonline(url)
	 
xbmcplugin.endOfDirectory(int(sys.argv[1]))
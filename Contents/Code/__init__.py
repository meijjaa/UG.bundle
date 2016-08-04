import lxml
import urllib2
from datetime import datetime

TITLE = 'NPO Uitzending Gemist'
BASE_URL = 'http://www.npo.nl/uitzending-gemist'
ROOT_URL = 'http://www.npo.nl'
HOST = 'www.npo.nl'
EPISODE_URL = '%s/afleveringen/%%s' % BASE_URL
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1'

####################################################################################################
def Start():
	Log("uzgv3: Loading plugin")
	#Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	#Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

	ObjectContainer.title1 = TITLE
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = USER_AGENT
	HTTP.Headers['Cookie'] = 'npo_cc=30'

####################################################################################################
@handler('/video/uzg3', TITLE)
def MainMenu():
	Log("uzgv3: Loading main menu")
	oc = ObjectContainer(no_cache=True)

	oc.add(DirectoryObject(key=Callback(Tips, title='Uitgelicht'), title='Uitgelicht'))
	oc.add(DirectoryObject(key=Callback(Days, title='Afgelopen week'), title='Afgelopen week'))
	oc.add(DirectoryObject(key=Callback(Viewed, title='Best bekeken afleveringen'), title='Best bekeken afleveringen'))
	oc.add(DirectoryObject(key=Callback(Genre, title='Afleveringen per Genre'), title='Afleveringen per Genre'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage,  url='%s/a-z/meest-bekeken?type=program&av_type=video' % (ROOT_URL), title='Best bekeken programma\'s'), title='Best bekeken programma\'s'))
	oc.add(DirectoryObject(key=Callback(AtoZ, title='Programma\'s A-Z'), title='Programma\'s A-Z'))

	# Do not show search on Rokus. Search finds mostly older videos which are all in M4V format (not HLS) and Roku playback always fails.
	#if Client.Platform not in ('Roku'):
	oc.add(SearchDirectoryObject(identifier='com.plexapp.plugins.uzgv3', title='Zoeken', prompt='Zoek uitzendingen', term='Uitzendingen'))

	return oc
	
####################################################################################################
@route('/video/uzg3/tips')
def Tips(title):
	
	tipsUrl =  BASE_URL + '/kijktips'
	Log("uzgv3: download items from " + tipsUrl)
	oc = ObjectContainer(title2=title, no_cache=True)

	for tip in HTML.ElementFromURL(tipsUrl).xpath('//div[@class="tips"]/div')[:10]:
		tipData = tip.find('div[@class="span8"]/a')
		title = tipData.find('h4').text.replace('  ', ' ').strip()
		Log(title)
		try:
			summary=tipData.find('p').text.strip()
		except:
			summary=''
		#Log(summary)
		url = '%s%s' % (ROOT_URL, tipData.get('href'))
		try:
			thumb = tip.find('div[@class="span4"]/div/a')
			thumbimg=thumb.find('img')
			thumbsrc=thumbimg.get('src')
			if(not thumbsrc.startswith('http:')):
				thumbsrc='http:%s' % (thumbsrc)
			Log(thumbsrc)
		except:
			thumbsrc=''
			#Log('No thumb available')

		#Log("uzgv3: located item with Url " + url)
		oc.add(VideoClipObject(
			url = url,
			title = title,
			summary = summary,
			thumb = thumbsrc
		))

	return oc


#http://www.npo.nl/zoeken?sort_date=11-12-2015&type=program&av_type=video
####################################################################################################
@route('/video/uzg3/days')
def Days(title):
	
	zoekUrl =  BASE_URL
	Log("uzgv3: download items from " + zoekUrl)
	oc = ObjectContainer(title2=title, no_cache=True)

	for day in HTML.ElementFromURL(zoekUrl).xpath('//select[@name="sort_date"]/option')[:8]:
		
		title = day.text.replace('  ', ' ').strip()
		Log(title)
		url = '%s/zoeken?sort_date=%s&type=program&av_type=video' % (ROOT_URL, day.get('value'))
		
		#Log("uzgv3: located item with Url " + url)
		if title=='Kies een datum':
			Log("ignore item")
		else:
			oc.add(DirectoryObject(
				key = Callback(BrowseByDay, title=title, url=url),
				title = title
			))

	return oc
	
####################################################################################################
@route('/video/uzg3/viewed')
def Viewed(title):

	gemistUrl =  BASE_URL
	Log("uzgv3: download items from " + gemistUrl)
	oc = ObjectContainer(title2=title, no_cache=True)

	for episode in HTML.ElementFromURL(gemistUrl).xpath('//div[@id="most-viewed"]/div[@class="content"]/div[@class="search-results most-viewed"]/div[@class="tiles large-tiles"]/div[@class="row-fluid non-responsive"]/div/div[@class="list-item tile"]'):
		Log("Found episodes")
		episodeData = episode.find('div[@class="contextual-main-title"]/a')
		title = episodeData.find('h3').text.replace('  ', ' ').strip()
		#Log(title)
		url = '%s%s' % (ROOT_URL, episodeData.get('href'))
		try:
			summary=episode.find('div[@class="description"]/h4/a/div[@class="contextual-title"]').text.strip()
		except:
			summary=''
		#Log(summary)
		try:
			thumb = episode.find('div[@class="image-container"]/a')
			thumbimg=thumb.find('img')
			thumbsrc=thumbimg.get('src')
			if(not thumbsrc.startswith('http:')):
				thumbsrc='http:%s' % (thumbsrc)
			Log(thumbsrc)
		except:
			thumbsrc=''
			#Log('No thumb available')

		#Log("uzgv3: located item with Url " + url)
		oc.add(VideoClipObject(
			url = url,
			title = title,
			summary = summary,
			thumb = thumbsrc
		))
	
	#if len(oc) < 1:
	#	return ObjectContainer(header="Geen programma's", message="De best bekeken aflevering kunnen niet worden gevonden")
		
	return oc
	
	BestProgr
####################################################################################################
@route('/video/uzg3/bestprogr')
def BestProgr(title):

	gemistUrl =  BASE_URL
	Log("uzgv3: download items from " + gemistUrl)
	oc = ObjectContainer(title2=title, no_cache=True)

	for episode in HTML.ElementFromURL(gemistUrl).xpath('//div[@id="most-viewed"]/div[@class="content"]/div[@class="search-results most-viewed"]/div[@class="tiles large-tiles"]/div[@class="row-fluid non-responsive"]/div/div[@class="list-item tile"]'):
		Log("Found episodes")
		episodeData = episode.find('div[@class="contextual-main-title"]/a')
		title = episodeData.find('h3').text.replace('  ', ' ').strip()
		#Log(title)
		url = '%s%s' % (ROOT_URL, episodeData.get('href'))
		try:
			summary=episode.find('div[@class="description"]/h4/a/div[@class="contextual-title"]').text.strip()
		except:
			summary=''
		#Log(summary)
		try:
			thumb = episode.find('div[@class="image-container"]/a')
			thumbimg=thumb.find('img')
			thumbsrc=thumbimg.get('src')
			if(not thumbsrc.startswith('http:')):
				thumbsrc='http:%s' % (thumbsrc)
			Log(thumbsrc)
		except:
			thumbsrc=''
			#Log('No thumb available')

		#Log("uzgv3: located item with Url " + url)
		oc.add(VideoClipObject(
			url = url,
			title = title,
			summary = summary,
			thumb = thumbsrc
		))
	
	#if len(oc) < 1:
	#	return ObjectContainer(header="Geen programma's", message="De best bekeken aflevering kunnen niet worden gevonden")
		
	return oc
	
####################################################################################################
@route('/video/uzg3/genre')
def Genre(title):
	zoekUrl =  BASE_URL
	Log("uzgv3: download items from " + zoekUrl)
	oc = ObjectContainer(title2=title, no_cache=True)

	for genre in HTML.ElementFromURL(zoekUrl).xpath('//select[@name="main_genre"]/option')[:8]:
		
		title = genre.text.replace('  ', ' ').strip()
		Log(title)
		url = '%s/zoeken?main_genre=%s&type=program&av_type=video' % (ROOT_URL, genre.get('value'))
		
		#Log("uzgv3: located item with Url " + url)
		if title=='Kies een genre':
			Log("ignore item")
		else:
			oc.add(DirectoryObject(
				key = Callback(BrowseByDay, title=title, url=url),
				title = title
			))

	return oc
	
####################################################################################################	
@route('/video/uzg3/AtoZ')
def AtoZ(title):
	oc = ObjectContainer(title2=title, no_cache=True)
	Log("uzgv3: Loading a-z menu")
	
	letterUrl = ROOT_URL + '/a-z/'

	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + '#', title='#'), title='#'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'a', title='A'), title='A'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'b', title='B'), title='B'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'c', title='C'), title='C'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'd', title='D'), title='D'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'e', title='E'), title='E'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'f', title='F'), title='F'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'g', title='G'), title='G'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'h', title='H'), title='H'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'i', title='I'), title='I'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'j', title='J'), title='J'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'k', title='K'), title='K'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'l', title='L'), title='L'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'm', title='M'), title='M'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'n', title='N'), title='N'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'o', title='O'), title='O'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'p', title='P'), title='P'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'q', title='Q'), title='Q'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'r', title='R'), title='R'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 's', title='S'), title='S'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 't', title='T'), title='T'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'u', title='U'), title='U'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'v', title='V'), title='V'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'w', title='W'), title='W'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'y', title='X'), title='X'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'x', title='Y'), title='Y'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url=letterUrl + 'z', title='Z'), title='Z'))
	return oc
	


#episode results	
####################################################################################################
@route('/video/uzg3/browse/day', page=int)
def BrowseByDay(title, url, page=1):
	if page > 1:
		pageurl = '%s?page=%d' % (url, page)
	else:
		pageurl = url

	oc = ObjectContainer(title2=title, no_cache=True)

	try:
		html = HTML.ElementFromURL(pageurl)
	except:
		return ObjectContainer(header="Error", message="Er ging iets fout bij het ophalen van data")

	for episode in html.xpath('//div[@class="list-item non-responsive row-fluid"]'):
		episodeData = episode.find('div[@class="span8"]/a')
		episodetitle=episodeData.find('h4').text.replace('  ', ' ').strip()
		Log(episodetitle)
		try:
			summary=episodeData.find('p').text.strip()
		except:
			summary=''
		Log(summary)
		episodeurl = '%s%s' % (ROOT_URL, episodeData.get('href'))
		Log(episodeurl)
		try:
			thumb = episode.find('div[@class="span4"]/div/a')
			thumbimg=thumb.find('img')
			thumbsrc=thumbimg.get('src')
			if(not thumbsrc.startswith('http:')):
				thumbsrc='http:%s' % (thumbsrc)
			Log(thumbsrc)
		except:
			thumbsrc=''
			Log('No thumb available')

		oc.add(VideoClipObject(
			url = episodeurl,
			title = episodetitle,
			summary = summary,
			thumb = thumbsrc
		))

	if len(oc) < 1:
		return ObjectContainer(header="Geen programma's", message="Er staan voor deze opdracht nog geen programma's op Uitzending Gemist")

	next_page = html.xpath('//a[text()="Volgende"]')

	if len(oc) >= 20:
		oc.add(NextPageObject(
			key = Callback(BrowseByDay, title=title, url=url, page=page+1),
			title = 'Meer...'
		))

	return oc

def GetPagedData(url , page, count, oc):
	htmlParser = lxml.etree.HTMLParser()
	headers = {
		'Accept': 'text/html, */*; q=0.01',
		'Accept-Encoding': 'gzip, deflate',
		"Accept-Language": "en-US,en;q=0.5",
		'User-Agent': USER_AGENT
	}

	req = urllib2.Request(url=url, headers=headers)
	r = urllib2.urlopen(req)
	html = lxml.etree.parse(r, htmlParser)
	m = html.xpath('//meta[@name="csrf-token"]')[0]
	csrf =  m.attrib['content']
	Log('Got csrf-token: %s' % csrf)
	m = html.xpath('//div[@class="search-results-list"]')[0]
	pages =  int(m.attrib['data-pages'])
	Log('Available pages: %d' % pages)

	if page > 1:
		page = page * count - 1
	if page + count < pages:
		pages = page + count

	headers = {
		'Accept': 'text/html, */*; q=0.01',
		'Accept-Encoding': 'gzip, deflate',
		"Accept-Language": "en-US,en;q=0.5",
		'Host' : HOST,
		'User-Agent': USER_AGENT,
		'Referer': url,
		'X-Requested-With': 'XMLHttpRequest',
		'X-CSRF-Token': csrf
	}

	ret = 0
	while page < pages:
		if page > 1:
			pageurl = '%s?page=%d' % (url, page)
		else:
			pageurl = url
		Log('Requesting %s ' % pageurl)
		page += 1

		try:
			req = urllib2.Request(url = pageurl, headers=headers)
			r = urllib2.urlopen(req)
			html = lxml.etree.parse(r, htmlParser)

			for episode in html.xpath('//div[@class="big-list-item list-item non-responsive row-fluid"]'):
				try:
					episodeData=episode.find('div[@class="span8"]/a')
					episodetitle=episodeData.find('h4').text.replace('  ', ' ').strip()
				except:
					return

				if len(episodetitle) < 1:
					return

				try:
					summary=episodeData.find('p').text.strip()
				except:
					summary=''
				programurl = '%s%s' % (ROOT_URL, episodeData.get('href'))
				try:
					thumb = episode.find('div[@class="span4"]/div/a')
					thumbimg=thumb.find('img')
					thumbsrc=thumbimg.get('src')
					if(not thumbsrc.startswith('http:') and len(thumbsrc) > 0):
						thumbsrc='http:%s' % (thumbsrc)
				except:
					thumbsrc=''

				oc.add(DirectoryObject(
					key=Callback(BrowseProgramm, url=programurl, title=episodetitle),
					title = episodetitle,
					summary = summary,
					thumb = thumbsrc
				))
			ret += 1
		except:
			break

	return ret


#programmas results
####################################################################################################
@route('/video/uzg3/browse/searchpage', page=int)
def BrowseResultsByPage(title, url, page=1):
	oc = ObjectContainer(title2=title, no_cache=True)#, view_group='List'

	ret = GetPagedData(url, page, 3, oc)
	Log('ret %d' % ret)
	if len(oc) < 1:
		return ObjectContainer(header="Geen programma's", message="Er staan voor deze opdracht nog geen programma's op Uitzending Gemist")

	if ret == 3:
		oc.add(NextPageObject(
			key = Callback(BrowseResultsByPage, title=title, url=url, page=page+1),
			title = 'Meer...'
		))

	return oc

#programmas results
####################################################################################################
@route('/video/uzg3/browse/programm')
def BrowseProgramm(title, url):

	pageurl = '%s' % (url)
	oc = ObjectContainer(title2=title, no_cache=True) #, view_group='List'

	try:
		html = HTML.ElementFromURL(pageurl)
	except:
		return ObjectContainer(header="Error", message="Er ging iets fout bij het ophalen van data")

	for episode in html.xpath('//div[@class="list-item non-responsive row-fluid"]'):
		episodeData = episode.find('div[@class="span8"]/a')
		episodetitle=episodeData.find('h4').text.replace('  ', ' ').strip()
		Log(episodetitle)
		try:
			summary=episodeData.find('p').text.strip()
		except:
			summary=''
		episodeurl = '%s%s' % (ROOT_URL, episodeData.get('href'))
		try:
			thumb = episode.find('div[@class="span4"]/div/a')
			episodestatus=''
			thumbimg=thumb.find('img')
			thumbsrc=thumbimg.get('src')
			if(not thumbsrc.startswith('http:')):
				thumbsrc='http:%s' % (thumbsrc)
			Log(thumbsrc)
		except:
			episodestatus=thumb.find('div').get('class')
			thumbsrc=''
			Log('No thumb available')

		try:
			dt = episodeData.find('h5').text.split(u' \xb7 ')[0].replace('mrt', 'mar').replace('okt', 'oct')
			from datetime import datetime
			airdate = datetime.strptime(dt[3:], '%d %b %Y %H:%M')
			Log('airdate: ' + str(airdate))
		except:
			airdate = datetime(1900, 1 , 1)

		if(episodestatus=='program-not-available'):
			Log(episodestatus)
		else:
			Log('Add oc ' + episodetitle)
			oc.add(VideoClipObject(
				url = episodeurl,
				title = episodetitle,
				summary = summary,
				thumb = thumbsrc,
				originally_available_at = airdate
			))
	if len(oc) < 1:
		return ObjectContainer(header="Geen afleveringen", message="Er staan voor deze serie nog geen afleveringen op Uitzending Gemist")

	return oc

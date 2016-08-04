TITLE = 'NPO Uitzending Gemist'
BASE_URL = 'http://www.npo.nl/uitzending-gemist'
ROOT_URL = 'http://www.npo.nl'
EPISODE_URL = '%s/afleveringen/%%s' % BASE_URL

####################################################################################################
def Start():
	Log("uzgv3: Loading plugin")
	#Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	#Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

	ObjectContainer.title1 = TITLE
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1'
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
	
	letterUrl = ROOT_URL + '/a-z'

	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s?type=program&av_type=video' % (letterUrl), title='#'), title='#'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/a?type=program&av_type=video' % (letterUrl), title='A'), title='A'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/b?type=program&av_type=video' % (letterUrl), title='B'), title='B'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/c?type=program&av_type=video' % (letterUrl), title='C'), title='C'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/d?type=program&av_type=video' % (letterUrl), title='D'), title='D'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/e?type=program&av_type=video' % (letterUrl), title='E'), title='E'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/f?type=program&av_type=video' % (letterUrl), title='F'), title='F'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/g?type=program&av_type=video' % (letterUrl), title='G'), title='G'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/h?type=program&av_type=video' % (letterUrl), title='H'), title='H'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/i?type=program&av_type=video' % (letterUrl), title='I'), title='I'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/j?type=program&av_type=video' % (letterUrl), title='J'), title='J'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/k?type=program&av_type=video' % (letterUrl), title='K'), title='K'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/l?type=program&av_type=video' % (letterUrl), title='L'), title='L'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/m?type=program&av_type=video' % (letterUrl), title='M'), title='M'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/n?type=program&av_type=video' % (letterUrl), title='N'), title='N'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/o?type=program&av_type=video' % (letterUrl), title='O'), title='O'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/p?type=program&av_type=video' % (letterUrl), title='P'), title='P'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/q?type=program&av_type=video' % (letterUrl), title='Q'), title='Q'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/r?type=program&av_type=video' % (letterUrl), title='R'), title='R'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/s?type=program&av_type=video' % (letterUrl), title='S'), title='S'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/t?type=program&av_type=video' % (letterUrl), title='T'), title='T'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/u?type=program&av_type=video' % (letterUrl), title='U'), title='U'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/v?type=program&av_type=video' % (letterUrl), title='V'), title='V'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/w?type=program&av_type=video' % (letterUrl), title='W'), title='W'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/x?type=program&av_type=video' % (letterUrl), title='X'), title='X'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/y?type=program&av_type=video' % (letterUrl), title='Y'), title='Y'))
	oc.add(DirectoryObject(key=Callback(BrowseResultsByPage, url='%s/z?type=program&av_type=video' % (letterUrl), title='Z'), title='Z'))
	return oc
	


#episode results	
####################################################################################################
@route('/video/uzg3/browse/day', page=int)
def BrowseByDay(title, url, page=1):

	pageurl = '%s&page=%d' % (url, page)
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

#programmas results
####################################################################################################
@route('/video/uzg3/browse/searchpage', page=int)
def BrowseResultsByPage(title, url, page=1):

	pageurl = '%s&page=%d' % (url, page)
	Log(pageurl)
	oc = ObjectContainer(title2=title, no_cache=True)

	try:
		html = HTML.ElementFromURL(pageurl)
	except:
		return ObjectContainer(header="Error", message="Er ging iets fout bij het ophalen van data")

	element = html.xpath('//div[@class="search-results"]/div')[:10][0]
	Log(element)
		
	for episode in html.xpath('//div[@class="search-results"]/div')[:10]:
		episodeData = episode.find('div[@class="span8"]/a')
		episodetitle=episodeData.find('h4').text.replace('  ', ' ').strip()
		Log(episodetitle)
		try:
			summary=episodeData.find('p').text.strip()
		except:
			summary=''
		Log(summary)
		programurl = '%s%s' % (ROOT_URL, episodeData.get('href'))
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
	
		oc.add(DirectoryObject(
			key=Callback(BrowseProgramm, url=programurl, title=episodetitle),
			title = episodetitle,
			summary = summary,
			thumb = thumbsrc
		))

	if len(oc) < 1:
		return ObjectContainer(header="Geen programma's", message="Er staan voor deze opdracht nog geen programma's op Uitzending Gemist")

	next_page = html.xpath('//a[text()="Volgende"]')

	if len(oc) >= 10:
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
		#Log(summary)
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
		if(episodestatus=='program-not-available'):
			Log(episodestatus)
		else:
			oc.add(VideoClipObject(
				url = episodeurl,
				title = episodetitle,
				summary = summary,
				thumb = thumbsrc
			))

	if len(oc) < 1:
		return ObjectContainer(header="Geen afleveringen", message="Er staan voor deze serie nog geen afleveringen op Uitzending Gemist")


	return oc

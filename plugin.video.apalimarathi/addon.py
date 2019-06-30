# ApaliMarathi Plugin by 

import os
import re
import urllib, urllib2
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import CommonFunctions
import HTMLParser, urlparse
import urlresolver
from urlparse import urljoin

import requests


common = CommonFunctions
common.plugin = "plugin.video.apalimarathi"
#common.dbg = True # Default
#common.dbglevel = 9 # Default

ADDON = xbmcaddon.Addon(id='plugin.video.apalimarathi')

APALIMARATHI_MOVIES_URL = "http://mtalky.com/"
APALIMARATHI_NATAKS_URL = "http://mtalky.com/"
APALIMARATHI_MOVIES_PAGE_URL = "http://mtalky.com/list.aspx?Show=Picture&page="
APALIMARATHI_MOVIES_ALPHA_URL = "http://mtalky.com/list.aspx?Show=Picture&NameStartWithLetter="
APALIMARATHI_NATAKS_ALPHA_URL = "http://mtalky.com/list.aspx?Show=Nataks&NameStartWithLetter="
APALIMARATHI_MOVIES_YEARS_URL = "http://mtalky.com/list.aspx?Show=Picture&ReleaseYear="
APALIMARATHI_NATAKS_PAGE_URL = "http://mtalky.com/list.aspx?Show=Nataks&page="
APALIMARATHI_ZEE_MARATHI_BASE_URL = "http://tvforumonline.com/"
APALIMARATHI_ZEE_MARATHI_URL = "http://tvforumonline.com/Guide.aspx?c=One"

def addDir(name, url, mode, iconimage, bannerImage='', lang='', infolabels=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&lang="+urllib.quote_plus(lang)+"&bannerImage="+urllib.quote_plus(bannerImage)+"&iconImage="+urllib.quote_plus(iconimage)
    #print iconimage
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    #liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    if infolabels != None:
       #liz.setInfo( type="Video", infoLabels={ "Plot": infolabels['Plot'], "Year": infolabels['Year'] } )
       liz.setInfo( type="Video", infoLabels=infolabels )

    liz.setProperty('IsPlayable', 'true')
    if len(bannerImage):
       liz.setProperty('fanart_image', bannerImage)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url, language, mode, iconimage, bannerimage):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/'
    addDir('Marathi Movies', '', 7, img_path + 'Marathi_Movies.png', 'marathi')
    addDir('Marathi Natak', '', 15, img_path + 'rangabhomi.jpg', 'marathi')
    addDir('Marathi TV Shows', '', 19, img_path + 'Marathi_Malika.png', 'marathi')
    addDir('Addon Settings', '', 13, img_path + 'settings.png', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

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

def inner_categories(name, url, language, mode, iconimage, bannerimage):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = 'lang=' + language + '&'
    postDataPage = '1'

    addDir('Recent', postDataPage, 3, img_path + 'recent.png', language)
    addDir('A-Z', postData, 8, img_path + 'a_z.png', language)
    addDir('Years', postData, 12, img_path + 'years.png', language)
    #addDir('Actors', postData, 10, img_path + 'actors.png', language)
    #addDir('Director', postData, 11, img_path + 'director.png', language)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def inner_natak_categories(name, url, language, mode, iconimage, bannerimage):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = 'lang=' + language + '&'
    postDataPage = '1'

    addDir('Recent', postDataPage, 16, img_path + 'recent.png', language)
    addDir('A-Z', postData, 17, img_path + 'a_z.png', language)
    #addDir('Years', postData, 12, img_path + 'years.png', language)
    #addDir('Actors', postData, 10, img_path + 'actors.png', language)
    #addDir('Director', postData, 11, img_path + 'director.png', language)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_recent_natak_list(name, url, language, mode, iconimage, bannerimage):
    cwd = ADDON.getAddonInfo('path')
    currentPage = int(url)
    print "input url-Page = [%d]" % currentPage
    ###html_string = common.fetchPage({"link": APALIMARATHI_NATAKS_PAGE_URL + str(currentPage)})
    html_string = requests.get(APALIMARATHI_NATAKS_PAGE_URL + str(currentPage)).text
    common.log(html_string)

    retMovies = get_movies_from_url(APALIMARATHI_NATAKS_PAGE_URL + str(currentPage))
    for i in range(0, len(retMovies)):
        addDir((retMovies[i]['Title']).encode('utf-8'), APALIMARATHI_NATAKS_URL + (retMovies[i]['Link']).encode('utf-8'), 9, (retMovies[i]['ImageLink']).encode('utf-8'))

    #Create the Next Page link
    ###page_div = common.parseDOM(html_string["content"], "div", attrs = { "id": "Main_ChildContent1_Panel1" })
    page_div = common.parseDOM(html_string, "div", attrs = { "id": "Main_ChildContent1_Panel1" })
    page_list = common.parseDOM(page_div, "a") #, ret = "href")
    print repr(page_list)
    #page_links_list = common.parseDOM(html_string, "a", attrs = { "class": "pageLink" })
    if len(page_list):
       print "Max Pages = %d " % len(page_list)
       if currentPage < len(page_list):
          addDir("Next >>", str(currentPage+1), 16, "http://psnc.org.uk/wp-content/uploads/2015/07/eps-arrow-yellow-next-250x255.png", '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_recent_list(name, url, language, mode, iconimage, bannerimage):
    cwd = ADDON.getAddonInfo('path')
    currentPage = int(url)
    print "input url-Page = [%d]" % currentPage
    #html_string = common.fetchPage({"link": APALIMARATHI_MOVIES_PAGE_URL + str(currentPage)})
    html_string = requests.get(APALIMARATHI_MOVIES_PAGE_URL + str(currentPage)).text
    common.log(html_string)

    retMovies = get_movies_from_url(APALIMARATHI_MOVIES_PAGE_URL + str(currentPage))
    for i in range(0, len(retMovies)):
        addDir((retMovies[i]['Title']).encode('utf-8'), APALIMARATHI_MOVIES_URL + (retMovies[i]['Link']).encode('utf-8'), 9, (retMovies[i]['ImageLink']).encode('utf-8'))

    #Create the Next Page link
    ###page_div = common.parseDOM(html_string["content"], "div", attrs = { "id": "Main_ChildContent1_Panel1" })
    page_div = common.parseDOM(html_string, "div", attrs = { "id": "Main_ChildContent1_Panel1" })
    page_list = common.parseDOM(page_div, "a") #, ret = "href")
    print repr(page_list)
    #page_links_list = common.parseDOM(html_string, "a", attrs = { "class": "pageLink" })
    if len(page_list):
       print "Max Pages = %d " % len(page_list)
       if currentPage < len(page_list):
          addDir("Next >>", str(currentPage+1), 3, "http://psnc.org.uk/wp-content/uploads/2015/07/eps-arrow-yellow-next-250x255.png", '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_movie_page(name, url, language, mode, iconimage, bannerimage):
    print "Showing Main Movie Page: " + name + ", with url:"+ url
    ###movie_page_html_string = common.fetchPage({"link": url})
    movie_page_html_string = requests.get(url).text
    ###print repr(movie_page_html_string["content"])
    print repr(movie_page_html_string)
    ###Need to figure out unicode font support
    #movie_name_list = common.parseDOM(movie_page_html_string["content"], "span", attrs = { "id": "Main_NameLabel" })
    #print (movie_name_list[0]).encode('utf-8')
    #addDir((movie_name_list[0]).encode('utf-8'), url, 2, '')
    ###movie_image_list = common.parseDOM(movie_page_html_string["content"], "img", attrs = { "id": "Main_imageResize1" }, ret = "src")
    movie_image_list = common.parseDOM(movie_page_html_string, "img", attrs = { "id": "Main_imageResize1" }, ret = "src")
    print (movie_image_list[0]).encode('utf-8')
    match = re.compile('img.ashx\?p=(.+?)\|').findall(movie_image_list[0])
    if len(match):
        banner_image_url = match[0]
    else:
        banner_image_url = movie_image_list[0]

    print "BANNER_IMG:" + banner_image_url

    #print "getProperty: " + self.list.getProperty("thumbnailImage")
    print "IMG:" + iconimage

    #get Movie Synopsis
    #movie_synopsis_list = common.parseDOM(movie_page_html_string, "div", attrs = { "id": "Main_DescriptionLabel" })
    #if len(movie_synopsis_list):
    #    print "Synopsis : " + (movie_synopsis_list[0]).encode('utf-8')


    #get the Form elements.
    ###viewstate_list = common.parseDOM(movie_page_html_string["content"], "input", attrs = { "id": "__VIEWSTATE" }, ret = "value")
    viewstate_list = common.parseDOM(movie_page_html_string, "input", attrs = { "id": "__VIEWSTATE" }, ret = "value")
    print (viewstate_list[0]).encode('utf-8')

    movie_sources_names_list = []
    #Find the movie sources - value
    ###movie_source_list = common.parseDOM(movie_page_html_string["content"], "input", attrs = { "type": "submit" }, ret = "value")
    movie_source_list = common.parseDOM(movie_page_html_string, "input", attrs = { "type": "submit" }, ret = "value")
    for i in range(0, len(movie_source_list)):
        movie_source_name = {}
        movie_source_name['value'] = movie_source_list[i]
        print (movie_source_list[i]).encode('utf-8')
        movie_sources_names_list.append(movie_source_name)

    #Find the movie sources - name
    ###movie_source_list = common.parseDOM(movie_page_html_string["content"], "input", attrs = { "type": "submit" }, ret = "name")
    movie_source_list = common.parseDOM(movie_page_html_string, "input", attrs = { "type": "submit" }, ret = "name")
    for i in range(0, len(movie_source_list)):
        movie_sources_names_list[i]['name'] = movie_source_list[i]

        #Find the first page URL by POSTing the form data
        ###l_post_data = { "__VIEWSTATE" : viewstate_list[0], "__SCROLLPOSITIONX" : "0", "__SCROLLPOSITIONY" : "400", "__EVENTTARGET" : "", movie_sources_names_list[i]['name'] : movie_sources_names_list[i]['value'].encode('utf-8') }
        l_post_data = { "__VIEWSTATE" : viewstate_list[0], "__SCROLLPOSITIONX" : "0", "__SCROLLPOSITIONY" : "400", "__EVENTTARGET" : "", movie_sources_names_list[i]['name'] : movie_sources_names_list[i]['value'].encode('utf-8') }
        ###movie_page_1_html_string = common.fetchPage({"link": url, "post_data" : l_post_data})
        movie_page_1_html_string = requests.post(url, data=l_post_data)
        ###print repr(movie_page_1_html_string["content"])
        #print movie_page_1_html_string
        print "redirect url: " + movie_page_1_html_string.url

        ###movie_sources_names_list[i]['Link'] = movie_page_1_html_string["new_url"].encode('utf-8')
        movie_sources_names_list[i]['Link'] = movie_page_1_html_string.url.encode('utf-8')
        print (movie_source_list[i]).encode('utf-8')

    for i in range(0, len(movie_sources_names_list)):
        #addDir((movie_sources_names_list[i]['value']).encode('utf-8'), (movie_sources_names_list[i]['Link']).encode('utf-8'), 10, banner_image_url.encode('utf-8'))
        addDir((movie_sources_names_list[i]['value']).encode('utf-8'), (movie_sources_names_list[i]['Link']).encode('utf-8'), 10, iconimage.encode('utf-8'), banner_image_url.encode('utf-8'))

    #addDir(name, url, 2, match[0].encode('utf-8'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#Shows all parts for selected Source
def show_movie_sources_page(name, url, language, mode, iconimage, bannerimage):
    print "Showing Parts Page for Soruce: " + name + ", with url:"+ url

    h = HTMLParser.HTMLParser()
    isLastPage = False
    #Start with the url of 1st part page
    part_page_url = url

    nParts = 0;
    #Loop until we reach the last page
    while isLastPage == False:
        nParts = nParts + 1
        #Fetch the part page from the URL
        ###part_page_html = common.fetchPage({"link": part_page_url})
        print "part_page_url: " + repr(part_page_url)
        part_page_html = requests.get(part_page_url).text
        print "part_page_url Read"
        #print "part_page_html: " + repr(part_page_html)

        #Parse the URL for the Main_EmbDiv to get movie Embed link Page
        ###part_embed_link_list = common.parseDOM(part_page_html["content"], "div", attrs = { "id": "Main_EmbDiv" })
        part_embed_link_list = common.parseDOM(part_page_html, "div", attrs = { "id": "Main_EmbDiv" })
	print " After Parsing part_page_html: "
        if len(part_embed_link_list):
           #print "Main_EmbDiv: " + repr(part_embed_link_list[0])
           match = re.compile('load\(\'(.+?)\'\)').findall(part_embed_link_list[0])
           if len(match):
              part_embed_url = urljoin(url, match[0])
              #print "PART URL:" + part_embed_url
              #Find the atual provided URL
              ###part_embed_html = common.fetchPage({"link": part_embed_url})
	      print "part_embed_url: " + repr(part_embed_url)
              part_embed_html = requests.get(part_embed_url).text
	      print "part_embed_url read: "
              #print "part_embed_html: " + repr(part_embed_html)
              ###part_iframe_src_list = common.parseDOM(part_embed_html["content"], "iframe", ret = "src")
              part_iframe_src_list = common.parseDOM(part_embed_html, "a", ret = "href")
	      print " After Parsing a - href part_embed_html: "
              if len(part_iframe_src_list):
                 print "a_href: " + repr(part_iframe_src_list[0])

                 addDir(name + " : Part %d" % nParts, part_iframe_src_list[0].encode('utf-8'), 2, iconimage, bannerimage)
	      else:
	         #search using the iframe src
	         part_iframe_src_list = common.parseDOM(part_embed_html, "iframe", ret = "src")
		 print " After Parsing iframe - src part_embed_html: "
                 if len(part_iframe_src_list):
                    print "iframe_src: " + repr(part_iframe_src_list[0])

                    addDir(name + " : Part %d" % nParts, part_iframe_src_list[0].encode('utf-8'), 2, iconimage, bannerimage)

        #Parse the URL for the Next Pages
        ###next_part_page_list = common.parseDOM(part_page_html["content"], "a", attrs = { "id": "Main_lnkNext"}, ret = "href")
        next_part_page_list = common.parseDOM(part_page_html, "a", attrs = { "id": "Main_lnkNext"}, ret = "href")
	print " After Parsing part_page_html 2: "
        if len(next_part_page_list):
           print "Next Page Partial URL: " + repr(next_part_page_list[0])
           #part_page_url = urljoin(url, urllib.quote_plus(h.unescape(next_part_page_list[0])))
           part_page_url = urlencode_local( urljoin(url, h.unescape(next_part_page_list[0])) )
           print "Next Page URL: " + repr(part_page_url)
        else:
           isLastPage = True

        if nParts >= 20: isLastPage = True #Just a termination condition for testing

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def urlencode_local(in_url):
    out_url = in_url
    p = urlparse.urlparse(in_url)
    out_url = urlparse.urlunsplit((p.scheme, p.netloc, p.path, urllib.quote(p.query, ':&='), p.fragment))
    return out_url

##
# Plays the video. Called when the id is 2.
##
def play_video(name, url, language, mode, iconimage, bannerimage):
    print "Playing: " + name + ", with url:"+ url
    stream_url = urlresolver.HostedMediaFile(url=url, host='', media_id='').resolve()
    if stream_url:
       print "Playing: stream_url:"+ stream_url
       playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
       playlist.clear()
       listitem = xbmcgui.ListItem(name)
       listitem.setThumbnailImage(iconimage)
       playlist.add(stream_url, listitem)
       xbmc.Player().play(playlist)
    else:
       print "No Video stream resolved for URL: " + url
       if url.find("vid.me") > 0:
          print "Trying to resolve for vid.me [%s]" % url
          html = common.fetchPage({"link": url})["content"]
          r = re.search('\<meta property.*og:video:url.*\s*content="([^"]+.mp4[^"]+)', html)
          if r:
             stream_url = r.group(1).replace('&amp;', '&')
             print "Playing: stream_url:"+ stream_url
             playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
             playlist.clear()
             listitem = xbmcgui.ListItem(name)
             listitem.setThumbnailImage(iconimage)
             playlist.add(stream_url, listitem)
             xbmc.Player().play(playlist)
       elif url.find("sendvid.com") > 0:
          print "Trying to resolve for sendvid.com [%s]" % url
          html = common.fetchPage({"link": url})["content"]
          #r = re.search('\<meta property.*og:video.*content=\"([^"]+.mp4)\"', html)
	  r = re.search('''var\s+video_source\s*=\s*['"](http.*?mp4.*)['"]''', html)
          if r:
             stream_url = r.group(1).replace('&amp;', '&')
             print "Playing: stream_url:"+ stream_url
             playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
             playlist.clear()
             listitem = xbmcgui.ListItem(name)
             listitem.setThumbnailImage(iconimage)
             playlist.add(stream_url, listitem)
             xbmc.Player().play(playlist)
       else:
          __addon__ = xbmcaddon.Addon()
          __addonname__ = __addon__.getAddonInfo('name')
          __icon__ = __addon__.getAddonInfo('icon')
 
          line1 = "Link Removed. Please try another one."
          time = 5000 #in miliseconds
 
          xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(name, url, language, mode, iconimage, bannerimage):
    azlist = map (chr, range(65,91))
    for letter in azlist:
        addDir(letter, letter, 11, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_natak_A_Z(name, url, language, mode, iconimage, bannerimage):
    azlist = map (chr, range(65,91))
    for letter in azlist:
        addDir(letter, letter, 18, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the List of movies for selected alphabet. Called when id is 11.
##
def show_movie_list_by_alpha(name, url, language, mode, iconimage, bannerimage):
    currentPage = url
    print "input url-Alphabet = [%s]" % currentPage
    retMovies = get_movies_from_url(APALIMARATHI_MOVIES_ALPHA_URL + currentPage)
    for i in range(0, len(retMovies)):
        addDir((retMovies[i]['Title']).encode('utf-8'), APALIMARATHI_MOVIES_URL + (retMovies[i]['Link']).encode('utf-8'), 9, (retMovies[i]['ImageLink']).encode('utf-8'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_natak_list_by_alpha(name, url, language, mode, iconimage, bannerimage):
    currentPage = url
    print "input url-Alphabet = [%s]" % currentPage
    retMovies = get_movies_from_url(APALIMARATHI_NATAKS_ALPHA_URL + currentPage)
    for i in range(0, len(retMovies)):
        addDir((retMovies[i]['Title']).encode('utf-8'), APALIMARATHI_NATAKS_URL + (retMovies[i]['Link']).encode('utf-8'), 9, (retMovies[i]['ImageLink']).encode('utf-8'))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_movies_from_url(urlIn):
    #html_string = common.fetchPage({"link": urlIn})
    html_string = requests.get(urlIn).text
    common.log(html_string)

    #Get the entire Movie DIV
    ###movie_div = common.parseDOM(html_string["content"], "div", attrs = { "class": "MovieDiv" })
    movie_div = common.parseDOM(html_string, "div", attrs = { "class": "MovieDiv" })

    movies = []

    #Parse Image divs
    movie_image_div_list = common.parseDOM(movie_div, "div", attrs = { "class": "imageDiv" })
    #print repr(movie_image_div_list)
    for i in range(0, len(movie_image_div_list)):
        movie = {}
        movie_image_div_href_list = common.parseDOM(movie_image_div_list[i], "a", ret = "href")
        movie['Link'] = movie_image_div_href_list[0]
        #print "%d> movie_image_div_href_list: " % i + repr(movie_image_div_href_list)
        movie_image_link = common.parseDOM(movie_image_div_list[i], "img", ret = "data-image")
        print "%d> movie_image_link: " % i + repr(movie_image_link[0])
        match = re.compile('Thumb120.ashx\?p=\s*(\S+?)\s*\|').findall(movie_image_link[0])
        movie['ImageLink'] = match[0]
        #print repr(movie_image_div_href_list), repr(movie_image_link)
        movies.append(movie)

    movie_span_list = common.parseDOM(movie_div, "span", attrs = { "class": "movieTitle" }) #, ret = "href")
    #print repr(movie_span_list)

    for i in range(0, len(movie_span_list)):
        movies[i]['Title'] = movie_span_list[i]
        print (movies[i]['Title']).encode('utf-8'), (APALIMARATHI_MOVIES_URL + movies[i]['Link']).encode('utf-8'), ((movies[i]['ImageLink']).encode('utf-8'))
    return movies

##
# Displays the options for A-Z view. Called when id is 8.
##
def show_Years(name, url, language, mode, iconimage, bannerimage):
    ###html_string = common.fetchPage({"link": APALIMARATHI_MOVIES_YEARS_URL + str(2015)})
    html_string = requests.get(APALIMARATHI_MOVIES_YEARS_URL + str(2015)).text
    common.log(html_string)

    #Get the entire Movie DIV
    ###years_div = common.parseDOM(html_string["content"], "div", attrs = { "id": "Main_ChildContent1_Year" })
    years_div = common.parseDOM(html_string, "div", attrs = { "id": "Main_ChildContent1_Year" })
    if len(years_div):
       available_years = common.parseDOM(years_div, "a")
       for i in range(0, len(available_years)):
          #Add Years
          addDir(available_years[i], available_years[i], 14, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the shows for Zee Marathi. Called when id is 20.
##
def show_zee_tv_shows(name, url, language, mode, iconimage, bannerimage):
    html_string = common.fetchPage({"link": APALIMARATHI_ZEE_MARATHI_URL})
    common.log(html_string)

    #Get the entire TV Shows DIV
    tv_shows_div = common.parseDOM(html_string["content"], "table", attrs = { "id": "MainContent_DataList2" })
    print repr(tv_shows_div)
    if len(tv_shows_div):
       available_shows = common.parseDOM(common.parseDOM(tv_shows_div, "a"), "span")
       for i in range(0, len(available_shows)):
          #Add Show
	  print (available_shows[i]).encode('utf-8')
          #addDir(available_shows[i], available_shows[i], 14, '')
       available_shows_href = common.parseDOM(tv_shows_div, "a", ret = "href")
       for i in range(0, len(available_shows_href)):
          #Add Show
	  print (available_shows_href[i]).encode('utf-8')
	  addDir((available_shows[i]).encode('utf-8'), APALIMARATHI_ZEE_MARATHI_BASE_URL + (available_shows_href[i]).encode('utf-8'), 21, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the available dates for selected TV Show. Called when id is 21.
##
def show_zee_tv_shows_dates(name, url, language, mode, iconimage, bannerimage):
    print "Showing Dates for url:[%s]" % url
    html_string = common.fetchPage({"link": url})
    common.log(html_string)

    #Get the entire TV Shows DIV
    tv_shows_dates_table = common.parseDOM(html_string["content"], "table", attrs = { "id": "MainContent_DataList2" })
    print repr(tv_shows_dates_table)
    if len(tv_shows_dates_table):
       available_show_dates = common.parseDOM(tv_shows_dates_table, "a")
       for i in range(0, len(available_show_dates)):
          #Add Show
	  print (available_show_dates[i]).encode('utf-8')
          #addDir(available_shows[i], available_shows[i], 14, '')
       available_show_dates_href = common.parseDOM(tv_shows_dates_table, "a", ret = "href")
       for i in range(0, len(available_show_dates_href)):
          #Add Show
	  print (available_show_dates_href[i]).encode('utf-8')
	  addDir((available_show_dates[i]).encode('utf-8'), APALIMARATHI_ZEE_MARATHI_BASE_URL + (available_show_dates_href[i]).encode('utf-8'), 24, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the available parts for selected TV Show. Called when id is 22.
##
def show_zee_tv_shows_parts_old(name, url, language, mode, iconimage, bannerimage):
    html_string = common.fetchPage({"link": url})
    common.log(html_string)

    #Get the entire TV Shows DIV
    tv_shows_parts_div = common.parseDOM(html_string["content"], "div", attrs = { "id": "MainContent_List" })
    #print repr(tv_shows_parts_div)
    if len(tv_shows_parts_div):
       available_show_parts = common.parseDOM(tv_shows_parts_div, "a")
       for i in range(0, len(available_show_parts)):
          #Add Show
	  print (available_show_parts[i]).encode('utf-8')
       available_show_parts_href = common.parseDOM(tv_shows_parts_div, "a", ret = "href")
       for i in range(0, len(available_show_parts_href)):
          #Add Show
	  print (available_show_parts_href[i]).encode('utf-8')
	  addDir((available_show_parts[i]).encode('utf-8'), APALIMARATHI_ZEE_MARATHI_BASE_URL + (available_show_parts_href[i]).encode('utf-8'), 23, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#Shows all parts for selected Date
def show_zee_tv_shows_parts(name, url, language, mode, iconimage, bannerimage):
    print "Showing Parts for date: " + name + ", with url:"+ url

    h = HTMLParser.HTMLParser()
    isLastPage = False
    #Start with the url of 1st part page
    part_page_url = url

    nParts = 0;
    #Loop until we reach the last page
    while isLastPage == False:
        nParts = nParts + 1
        #Fetch the part page from the URL
        part_page_html = common.fetchPage({"link": part_page_url})
        #print "part_page_html: " + repr(part_page_html["content"])

        #Parse the URL for the MainContent_List to get movie Embed link Page
        part_embed_link_list = common.parseDOM(part_page_html["content"], "div", attrs = { "id": "MainContent_List" })
        if len(part_embed_link_list):
           #print "Main_EmbDiv: " + repr(part_embed_link_list[0])
           match = re.compile('load\(\'(.+?)\'\)').findall(part_embed_link_list[0])
           if len(match):
              part_embed_url = urljoin(url, match[0])
              #print "PART URL:" + part_embed_url
              #Find the atual provided URL
              part_embed_html = common.fetchPage({"link": part_embed_url})
              #print "part_embed_html: " + repr(part_embed_html["content"])
              part_iframe_src_list = common.parseDOM(part_embed_html["content"], "iframe", ret = "src")
              if len(part_iframe_src_list):
                 print "iframe_src: " + repr(part_iframe_src_list[0])

                 addDir(name + " : Part %d" % nParts, part_iframe_src_list[0].encode('utf-8'), 2, iconimage, bannerimage)

        #Parse the URL for the Next Pages
        next_part_page_div = common.parseDOM(part_page_html["content"], "div", attrs = { "id": "MainContent_nPart"})
        if len(next_part_page_div):
           next_part_page_list = common.parseDOM(next_part_page_div[0], "a", ret = 'href')
           if len(next_part_page_list):
              print "Next Page Partial URL: " + repr(next_part_page_list[0])
              #part_page_url = urljoin(url, urllib.quote_plus(h.unescape(next_part_page_list[0])))
              part_page_url = urlencode_local( urljoin(url, h.unescape(next_part_page_list[0])) )
              print "Next Page URL: " + repr(part_page_url)
           else:
              isLastPage = True
        else:
           isLastPage = True

        if nParts >= 20: isLastPage = True #Just a termination condition for testing

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_tv_show_part_video_url(name, url, language, mode, iconimage, bannerimage):
    part_page_html = common.fetchPage({"link": url})
    #print "Input url-[%s]" % url
    #print "part_page_html-[%s]" % part_page_html["content"].encode('utf-8')
    #Parse the URL for the MainContent_content1 to get movie Embed link Page
    part_embed_link_list = common.parseDOM(part_page_html["content"], "div", attrs = { "id": "MainContent_content1" })
    if len(part_embed_link_list):
       #print "Main_EmbDiv: " + repr(part_embed_link_list[0])
       match = re.compile('load\(\'(.+?)\'\)').findall(part_embed_link_list[0])
       if len(match):
          part_embed_url = urljoin(url, match[0])
          #print "PART URL:" + part_embed_url
          #Find the atual provided URL
          part_embed_html = common.fetchPage({"link": part_embed_url})
          #print "part_embed_html: " + repr(part_embed_html["content"])
          part_iframe_src_list = common.parseDOM(part_embed_html["content"], "iframe", ret = "src")
          if len(part_iframe_src_list):
             print "iframe_src: " + repr(part_iframe_src_list[0])
             play_video(name, part_iframe_src_list[0].encode('utf-8'), language, mode, iconimage, bannerimage)

##
# Displays the List of movies for selected year. Called when id is 14.
##
def show_movie_list_by_year(name, url, language, mode, iconimage, bannerimage):
    currentYear = url
    print "input url-Alphabet = [%s]" % currentYear
    retMovies = get_movies_from_url(APALIMARATHI_MOVIES_YEARS_URL + currentYear)
    for i in range(0, len(retMovies)):
        addDir((retMovies[i]['Title']).encode('utf-8'), APALIMARATHI_MOVIES_URL + (retMovies[i]['Link']).encode('utf-8'), 9, (retMovies[i]['ImageLink']).encode('utf-8'), infolabels={'Year': str(currentYear), 'Plot': ''} )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for A-Z view. Called when id is 8.
##
def show_settings(name, url, language, mode, iconimage, bannerimage):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Prints the TV Channel list. Called when id is 19.
##
def show_tv_channels(name, url, language, mode, iconimage, bannerimage):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/'
    addDir('ZEE Marathi', '', 20, img_path + 'Zee_Marathi.jpg', 'marathi')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

params=get_params()
url=''
name=''
mode=0
language=''
bannerimage=''
iconimage=''

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

try:
    language=urllib.unquote_plus(params["lang"])
except:
    pass

try:
    bannerimage=urllib.unquote_plus(params["bannerImage"])
except:
    pass

try:
    iconimage=urllib.unquote_plus(params["iconImage"])
except:
    pass

# Modes
# 0: The main Categories Menu. Selection of language
# 2: Play the video
# 3: The Recent Section
# 7: Sub menu
# 8: A-Z view
# 9: show_movie_page
#10: show_movie_sources_page
#11: show_movie_list_by_alpha
#12: show_Years
#13: show_settings
#14: show_movie_list_by_year
#15: inner_natak_categories
#16: show_recent_natak_list
#17: show_natak_A_Z
#18: show_natak_list_by_alpha
#19: show_tv_channels
#20: show_zee_tv_shows
#21: show_zee_tv_shows_dates
#22: show_zee_tv_shows_parts_old
#23: get_tv_show_part_video_url
#24: show_zee_tv_shows_parts

function_map = {}
function_map[0] = main_categories
function_map[2] = play_video
function_map[3] = show_recent_list
function_map[7] = inner_categories
function_map[8] = show_A_Z
function_map[9] = show_movie_page
function_map[10] = show_movie_sources_page
function_map[11] = show_movie_list_by_alpha
function_map[12] = show_Years
function_map[13] = show_settings
function_map[14] = show_movie_list_by_year
function_map[15] = inner_natak_categories
function_map[16] = show_recent_natak_list
function_map[17] = show_natak_A_Z
function_map[18] = show_natak_list_by_alpha
function_map[19] = show_tv_channels
function_map[20] = show_zee_tv_shows
function_map[21] = show_zee_tv_shows_dates
function_map[22] = show_zee_tv_shows_parts_old
function_map[23] = get_tv_show_part_video_url
function_map[24] = show_zee_tv_shows_parts

function_map[mode](name, url, language, mode, iconimage, bannerimage)

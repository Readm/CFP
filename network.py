#! /usr/bin/python
# coding:utf-8
import urllib
import urllib2

def get(url,data=None):
    try:
        res = urllib2.urlopen(url, data)
        return res.read()
    except Exception,e:
        print "Network error,",e
        return ""

def search(keyword, year='this'):
    '''Return the url of search. year: 'this', 'next', 'forward', 'all'. '''
    year = year[0]
    keyword = urllib.urlencode(keyword)
    return "http://www.wikicfp.com/cfp/servlet/tool.search?q=%s&year=%s"%(keyword,year)

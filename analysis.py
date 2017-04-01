#! /usr/bin/python
# coding:utf-8

from bs4 import BeautifulSoup
import time

from network import *


class cfp():
    name = ''
    cfp_url = ''
    url = ''
    series = ''
    categories = ''
    full_name = ''
    where = ''
    when = time.localtime(0)
    deadline = time.localtime(0)
    notification = time.localtime(0)
    final_version = time.localtime(0)

    ccf_class = ''  # 'A','B','C',''

    def __init__(self):
        pass

    def __str__(self):
        str = ''
        str += 'Name: %s \n' % self.name.__str__()
        str += 'CFP_URL: %s \n' % self.cfp_url.__str__()
        str += 'Event ID: %s \n' % self.event_id.__str__()
        str += 'URL: %s \n' % self.url.__str__()
        str += 'Series: %s \n' % self.series.__str__()
        str += 'Categories: %s \n' % self.categories.__str__()
        str += 'Full name: %s \n' % self.full_name.__str__()
        str += 'Where: %s \n' % self.where.__str__()
        str += 'When: %s \n' % (time.strftime('%d %b %Y', self.when) if self.when != time.localtime(0) else 'N/A')
        str += 'Deadline: %s \n' % (
        time.strftime('%d %b %Y', self.deadline) if self.when != time.localtime(0) else 'N/A')
        str += 'Notification: %s \n' % (
        time.strftime('%d %b %Y', self.notification) if self.when != time.localtime(0) else 'N/A')
        str += 'Final version: %s \n' % (
        time.strftime('%d %b %Y', self.final_version) if self.when != time.localtime(0) else 'N/A')
        str += 'CCF: %s \n' % self.ccf_class.__str__()
        return str

    @property
    def event_id(self):
        id = 0
        if self.cfp_url:
            try:
                id = int(self.cfp_url.split('=')[-1])
            except:
                id = 0
        return id

    @property
    def year(self):
        return self.when[0]

    def get_more_info(self):
        pass

    def get_cfp_page(self):
        if self.cfp_url:
            return get(self.cfp_url)
        else:
            return None

    @classmethod
    def update(cls):
        pass




def search_return_list(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.html.body.find("div", {'class': 'contsec'})

    return_lst = []
    line_no = 0

    name = ''
    cfp_url = ''
    full_name = ''

    for tr in table.table.find_all('tr')[3:]:
        if line_no % 2 == 0:  # first line
            name = tr.a.string
            cfp_url = 'www.wikicfp.com' + tr.a.get('href').split('&')[0]
            full_name = tr.find_all('td')[-1].string
        else:  # second line
            when_str, where, deadline_str = [i.string for i in tr.find_all()]
            # update

            when = time.strptime(when_str.split('-')[0].strip(), "%b %d, %Y") \
                if when_str != 'N/A' else time.localtime(0)
            deadline = time.strptime(deadline_str.split('(')[0].strip(), "%b %d, %Y") \
                if when_str != 'N/A' else time.localtime(0)

            c = cfp()
            c.name = name
            c.cfp_url = cfp_url
            c.full_name = full_name
            c.when = when
            c.where = where
            c.deadline = deadline

            return_lst.append(c)
        line_no += 1
    return return_lst



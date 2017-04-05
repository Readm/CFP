#! /usr/bin/python
# coding:utf-8

from bs4 import BeautifulSoup
import time

from network import *

parser = 'html.parser'

class cfp():
    name = ''
    cfp_url = ''
    url = ''
    series = ''
    categories = ''
    full_name = ''
    where = ''
    when = 'N/A'
    deadline = 'N/A'
    notification = 'N/A'
    final_version = 'N/A'
    info = ''

    ccf_class = ''  # 'A','B','C',''

    def __init__(self):
        pass

    def reencode(self):
        for item in ['name','full_name']:
            new = getattr(self,item)
            new = new.encode(errors='ignore')
            new = new.decode(errors='ignore')
            setattr(self,item,new)

    def __str__(self):
        self.reencode()
        str = u''
        str += u'Name: %s \n' % self.name
        str += u'CFP_URL: %s \n' % self.cfp_url
        str += u'Event ID: %s \n' % self.event_id
        str += u'URL: %s \n' % self.url
        str += u'Series: %s \n' % self.series
        str += u'Categories: %s \n' % self.categories
        str += u'Full name: %s \n' % self.full_name
        str += u'Where: %s \n' % self.where
        str += u'When: %s \n' % (time.strftime('%d %b %Y', self.when) if self.when != 'N/A' else 'N/A')
        str += u'Deadline: %s \n' % (time.strftime('%d %b %Y', self.deadline) if self.deadline!= 'N/A' else 'N/A')
        str += u'Notification: %s \n' % (time.strftime('%d %b %Y', self.notification) if self.notification != 'N/A' else 'N/A')
        str += u'Final version: %s \n' % (time.strftime('%d %b %Y', self.final_version) if self.final_version != 'N/A' else 'N/A')
        str += u'CCF: %s \n' % self.ccf_class
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
            return get('http://'+self.cfp_url)
        else:
            return None

    def update(self):
        cfp_page = self.get_cfp_page()
        soup = BeautifulSoup(cfp_page, parser)
        center = soup.html.body.find("div", {'class': 'contsec'}).center
        try:
            self.series = center.h3.next_sibling.next_sibling.next_sibling.next_sibling.string
        except:
            self.series = ''

        link_block = center.tr.next_sibling.next_sibling.next_sibling.next_sibling
        self.url = link_block.a.string

        table = link_block.next_sibling.next_sibling.next_sibling.next_sibling.find('table',{'class':'gglu'})
        cat = table.find_next('table',{'class':'gglu'}).h5.children.next()
        self.categories = cat.next_sibling.next_sibling.text

        self.when = table.find('th',text='When').next_sibling.next_sibling.string.strip()
        self.where = table.find('th',text='Where').next_sibling.next_sibling.string.strip()
        self.deadline = table.find('th',text='Submission Deadline').find_next('span',{'property':"v:startDate"}).string
        self.notification = table.find('th',text='Notification Due').find_next('span',{'property':"v:startDate"}).string
        self.final_version = table.find('th',text='Final Version Due').find_next('span',{'property':"v:startDate"}).string
        #self.info = center.find_next('div',{'class':'cfp'})
        # here, the parser drop the text, how to fix it ????

        self.convert_time()

    def convert_time(self):
        if not isinstance(self.when, time.struct_time):
            self.when = time.strptime(self.when.split('-')[0].strip(), "%b %d, %Y") \
                if self.when != 'N/A' else 'N/A'

        for item in ['deadline', 'final_version', 'notification']:
            if not isinstance(getattr(self, item),time.struct_time):
                s = getattr(self, item)
                t = time.strptime(s.split('(')[0].strip(), "%b %d, %Y") \
                    if s != 'N/A' else 'N/A'
                setattr(self,item,t)

    @classmethod
    def search_return_list(cls,html):
        soup = BeautifulSoup(html, parser)
        table = soup.html.body.find('table', {'cellpadding': '5', 'cellspacing': '2'})

        return_lst = []
        line_no = 0

        name = ''
        cfp_url = ''
        full_name = ''

        for tr in table.table.find_all('tr',recursive=False)[1:]:
            if line_no % 2 == 0:  # first line
                name = tr.a.string
                cfp_url = 'www.wikicfp.com' + tr.a.get('href').split('&')[0]
                full_name = tr.find_all('td')[-1].string
            else:  # second line
                when, where, deadline = [i.string for i in tr.find_all()]
                # update

                c = cfp()
                c.name = name
                c.cfp_url = cfp_url
                c.full_name = full_name
                c.when = when
                c.where = where
                c.deadline = deadline
                c.convert_time()

                return_lst.append(c)
            line_no += 1
        return return_lst

for i in cfp.search_return_list(get(search_url('Digital'))):
    print i
c = cfp.search_return_list(get(search_url('Digital')))[0]
c.update()


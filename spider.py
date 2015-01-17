#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ISJ project 2013/2014: Finding and downloading reports of research projects
# Author: Martin Veselovsky, xvesel60
# -----------------------------------

import urllib.request, urllib.error, re, os, argparse

DOWNLOAD_DIR = 'downloads/'
DOWNLOAD_PATH = DOWNLOAD_DIR
WEBPAGE_SUFFIXES = ['html', 'htm', 'jhtml', 'phtml', 'php', 'asp', 'aspx', 'jsp', 'xml']


def download_file(name, url):
    """ Download file from url to specified path """
    name, headers = urllib.request.urlretrieve(url, DOWNLOAD_PATH + name)
    return name


#region VISITED
class LList(list):
    """ Local List """
    def append(self, item):
        super(LList, self).append(item)
        print(item)

class RList(LList):
    """ Remote usage of list - GUI callback """
    def __init__(self, remote_method):
        super(RList, self).__init__()
        self.remote_method = remote_method

    def append(self, item):
        super(RList, self).append(item)
        self.remote_method(item)
#endregion

#region RESULTS
class LDict(dict):
    """ Local dict """
    def __init__(self, downloading):
        super(LDict, self).__init__()
        self.downloading = downloading

    def __setitem__(self, key, value):
        super(LDict, self).__setitem__(key, value)
        if self.downloading:
            download_file(key, value)

    def __getitem__(self, item):
        return super(LDict, self).__getitem__(item)

class RDict(dict):
    """ Remote usage dictionary - GUI callback """
    def __init__(self, remote_method):
        super(RDict, self).__init__()
        self.remote_method = remote_method

    def __setitem__(self, key, value):
        if not key in self:
            self.remote_method(value, key)
        super(RDict, self).__setitem__(key, value)
#endregion


class Spider():
    """
    Get all links from given url
    """

    def __init__(self, main_url, insert_to_visited=None, insert_to_results=None, downloading=False):
        global DOWNLOAD_PATH

        self.main_url = main_url + '/' if main_url[-1] != '/' else main_url
        self.to_visit = set()
        self.to_visit.add(main_url)
        self.visited  = RList(insert_to_visited) if insert_to_visited else LList()
        self.results  = RDict(insert_to_results) if insert_to_results else LDict(downloading)
        self.cancel = False

        # create directory for main_url's reports downloading
        dirname = main_url[:main_url.rfind('.')]
        DOWNLOAD_PATH = DOWNLOAD_DIR + dirname[dirname.rfind('.')+1:] + '/'
        if not os.path.exists(DOWNLOAD_PATH):
            os.mkdir(DOWNLOAD_PATH)

    def make_path(self, current_url, link):
        """
        Check path dependencies and recreate absolute path from relative
        :return: absolute path of link
        """

        # append slash
        current_url = current_url + '/' if current_url[-1] != '/' else current_url

        # return main_url
        if len(link) == 0:
            return self.main_url

        # move up to get corresponding url
        # e.g.  ../../lala.html
        elif link[0] == '.':
            current_url = current_url[:-1]
            for up in range(link.count('../') + 1):
                current_url = current_url[:current_url.rfind('/')]
            return current_url + '/' + link[link.rfind('../')+3:]

        # append main url
        elif link[0] == '/':
            return self.main_url + link[1:]

        # append current url
        else:
            if current_url != self.main_url:
                current_url = current_url[:-1]
                return current_url[:current_url.rfind('/')] + '/' + link
            else:
                return current_url + link


    def check_name(self, name, link, pretext):
        """
        Create pretty name
        :return: New formatted name
        """
        m = name.replace('&amp;', '').replace('&', '').replace('_', ' ')
        m = re.sub('<[^>]+>', '', m)
        if len(m) == 0:
            m = link[link.rfind('/')+1:link.rfind('.')]
        if pretext:
            p = re.sub('\s{2,}', ' ', pretext.strip())
            if len(p) > 0:
                m = p + '. ' + m.title()

        return m.title()


    def get(self):
        """
        Iterate over all links and gather new ones. Store visited links and results.
        """
        while len(self.to_visit) > 0:
            if self.cancel:
                break

            current_url = self.to_visit.pop()
            self.visited.append(current_url)

            # get html site
            try:
                response = urllib.request.urlopen(current_url)
                site = response.read().decode()
            except urllib.error.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except urllib.error.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)

            # find all links
            links = re.findall('([^>]*)<a.*?href=(?:"|\')(/?.+?)(?:"|\').*?>\s*(.+?)\s*<', site, re.DOTALL)
            for pretext, link, name in links:

                # remove useless
                if link.find('#') != -1:
                    link = link[:link.find('#')]

                # make absolute path from relative
                if link.find('http') == -1:
                    if link.find('mailto:') != -1:
                        continue
                    link = self.make_path(current_url, link)

                # skip links to another websites
                if link.find(self.main_url) == -1:
                    continue

                # reports
                if link.find('.pdf') != -1 or link.find('.doc') != -1 or link.find('.docx') != -1:
                    name = self.check_name(name, link, pretext)
                    self.results[link] = name

                # more links
                elif not link in self.visited:

                    r = re.search('/[^\.]+(\.\w+)?$', link, re.MULTILINE)

                    # validate suffix
                    if r and r.group(1) != None:
                        if r.group(1)[1:] in WEBPAGE_SUFFIXES:
                            self.to_visit.add(link)
                        else:
                            pass
                    # without suffix
                    else:
                        self.to_visit.add(link)


        print('RESULTS:')
        for k, v in self.results.items():
            print(v.ljust(50) + ' ' + k)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get all links of website and find research reports.')
    parser.add_argument('url', help='Url of website')
    parser.add_argument('-d', '--download', action='store_true', help='Immediate downloading')
    args = parser.parse_args()

    #url = 'http://www.weknowit.eu/'
    #url = 'http://www.kiwi-project.eu/'
    #url = 'http://www.kiwi-project.eu/kiwi/publications/33-deliverables.html'

    s = Spider(args.url, downloading=args.download)
    s.get()

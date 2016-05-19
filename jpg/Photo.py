#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import urllib
import threading


class PHOTO(object):
    """docstring for PHOTO"""
    def __init__(self, url, filename):
        super(PHOTO, self).__init__()
        print 'th:' + str(threading.activeCount())
        self.save(url, filename)

    def save(self, url, filename):
        # get extension
        if filename[-4:] != '.jpg':
            filename += '.jpg'
        # Download file
        th = threading.Thread(target=self.download, args=(url, filename))
        th.start()

    def download(self, url, filename):
        urllib.urlretrieve(url, filename)

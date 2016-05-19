#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import urllib
import threading


class VIDEO(object):
    """docstring for VIDEO"""
    def __init__(self, mediaStatus, filename):
        super(VIDEO, self).__init__()
        self.save(mediaStatus, filename)

    def save(self, mediaStatus, filename):
        # get url
        media_variants = mediaStatus['video_info']['variants']
        # get filename
        if filename[-4:] != '.mp4':
            filename += '.mp4'
        # download
        th = threading.Thread(
            target=self.download,
            args=(media_variants, filename)
        )
        th.start()

    def download(self, variants, filename):
        maxRate = 0
        # ef = ErrorPlace+'error_'+str(random.randint(0, 100))+'.txt'
        # with open(ef, 'w') as f:
        #     f.write(str(media_variants))
        # loop of variants
        for i in variants:
            # check that rate is max rate
            # print variant['url']
            try:
                cont_type = i['content_type']
                rate = i['bitrate']
                if (cont_type == 'video/mp4') and (rate > maxRate):
                    maxRate = i['bitrate']
                    url = i['url']
            except:
                pass
        # Download
        urllib.urlretrieve(url, filename)
        print "Finish Download!!"
        print "=> Came MP4 data!!"

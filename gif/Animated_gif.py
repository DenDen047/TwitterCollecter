#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import os
import urllib
import threading

from moviepy import editor


class GIF(object):
    """docstring for GIF"""
    def __init__(self, mediaStatus, filename):
        super(GIF, self).__init__()
        self.save(mediaStatus, filename)

    def save(self, mediaStatus, filename):
        # get filename which doesn't have the extension
        if filename[-4:] != '.gif':
            filename = filename.rstrip('.gif')
        url = mediaStatus['video_info']['variants'][0]['url']
        # Download file
        th = threading.Thread(target=self.download, args=(url, filename))
        th.start()

    def download(self, url, filename):
        # Download video
        dummy_mp4 = filename + '.mp4'
        urllib.urlretrieve(url, dummy_mp4)
        # Convert gif
        try:
            clip = editor.VideoFileClip(dummy_mp4)
            clip.write_gif(filename+".gif")
            os.remove(dummy_mp4)
        except:
            print "miss transform to gif"
        print "Finish Processing!!"
        print "=> Came GIF data!!"

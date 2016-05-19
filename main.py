#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

# --- readme ---
# This program is CollectingImageProgram by twitter.
# This needs a file and a folder; "APIkey.txt" and "images".
# "APIkey.txt" is APIkey file which contens
# ConsumerKey, ConsumerSecret, AccessToken and AccessTokenSecret.
# "images" is a folder to save collected images.
# And this program can display your TL!!
#
# --- Preparation ---
# pip install tweepy
#
#
# --- python 2.7.9
# --- 2015/05/13
#
# --- MuramatsuNaoya


import sys
import time
import logging
import urllib
import tweepy
from tweepy import Stream, TweepError
from datetime import datetime as dt

from init.Init import INIT
from jpg.Photo import PHOTO
from mp4.Video import VIDEO
from gif.Animated_gif import GIF


auth = None    # declare GlobalValuable

# defalut setting
ImageFolderPlace = ""
GifFolderPlace = ""
VideoFolderPlace = ""
ErrorPlace = ""
TrashPlace = ""
Dirs = {}


# === Processing of tweets ===
class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            t1 = time.time()
            # Display the text
            # print(
            #     "\n\n\n===@%s===\n---\n%s\n---"
            #     % (status.author.screen_name, status.text.strip())
            # )

            if status.text[0:2] == "RT":    # without retweet
                pass
            else:
                if 'media' in status.entities:
                    medias = status.extended_entities['media']  # get status
                    # loop to get images
                    if len(medias) != 1:
                        print len(medias)
                    cnt = 0
                    for x in medias:
                        # get image url
                        media_url = x['media_url']
                        # save the image
                        try:
                            time_now = dt.now()
                            timeStr = time_now.strftime('%Y%m%d%H%M%S')
                            xType = x['type']
                            # --- PHOTO ---
                            if xType == "photo":
                                filename = Dirs['jpg_place']+timeStr+str(cnt)
                                PHOTO(media_url, filename)

                            # --- GIF ---
                            elif xType == "animated_gif":
                                filename = Dirs['gif_place'] + timeStr
                                GIF(x, filename)

                            # --- VIDEO ---
                            elif xType == "video":
                                filename = Dirs['mp4_place'] + timeStr
                                VIDEO(x, filename)

                            # other
                            else:
                                print media_url
                                print x
                                print "type : %s" % (xType)
                            cnt += 1
                        except IOError:
                            print ">>> Failed to save!! <<<"
            # Display processing time
            diff = time.time() - t1
            if diff > 0.50:
                print "ProcessingTime : %s" % str(diff)
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True    # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True    # Don't kill the stream


# === UserStream ===
class UserStream(Stream):

    def user_stream(
        self,
        follow=None,
        track=None,
        async=False,
        locations=None
    ):
        self.parameters = {"delimited": "length", }
        self.headers['Content-type'] = "application/x-www-form-urlencoded"

        if self.running:
            raise TweepError('Stream object already connected!')

        self.scheme = "https"
        self.host = 'userstream.twitter.com'
        self.url = '/2/user.json'

        if follow:
            self.parameters['follow'] = ','.join(map(str, follow))
        if track:
            self.parameters['track'] = ','.join(map(str, track))
        if locations and len(locations) > 0:
            assert len(locations) % 4 == 0
            result = ','.join(['%.2f' % l for l in locations])
            self.parameters['locations'] = result

        self.body = urllib.urlencode(self.parameters)
        logging.debug(
            "[ User Stream URL ]: %s://%s%s"
            % (self.scheme, self.host, self.url)
        )
        logging.debug("[ Request Body ] :" + self.body)
        self._start(async)


# === MAIN ===
def main():
    global Dirs
    # init
    x = INIT('./setting.json')
    Dirs = x.pref

    print "\n\n-------------------\n"
    print "Start Collecting Image..."
    stream = UserStream(x.auth, CustomStreamListener())
    stream.timeout = None
    stream.user_stream()


if __name__ == "__main__":
    main()
    sys.exit()

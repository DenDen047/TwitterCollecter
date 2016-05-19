#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: cp932 -*-

import os
import json

import tweepy


# load setting.json
class LoadSetting(object):
    """docstring for LoadSetting"""
    def __init__(self, jsonFile):
        super(LoadSetting, self).__init__()
        self.setting = self.load(jsonFile)

    def load(self, jsonFile):
        # fix path
        jsonFile = os.path.expanduser(jsonFile)
        # open json file
        try:
            with open(jsonFile, 'r') as f:
                x = json.load(f)
        except:
            print u"設定ファイルが開けません"
            raise
        for k, v in x.items():
            x[k] = os.path.expanduser(v)
        return x


# load API.txt
class LoadAPI(object):
    """docstring for LoadAPI"""
    def __init__(self, default_key):
        super(LoadAPI, self).__init__()
        self.auth = self.load(default_key)

    # === File and Directory palce ===
    def load(self, default_key):
        # About APIkey
        while True:
            try:
                # The file's place searching...
                default_key = os.path.expanduser(default_key)
                # The file which have APIkey reading...
                with open(default_key) as keyFile:
                    keyList = keyFile.readlines()
                # Extracting APIkey...
                print "\nAPIkey is "
                for key in keyList:
                    print "    " + key.strip()
                # set API key
                auth_value = tweepy.OAuthHandler(
                    keyList[0].strip(), keyList[1].strip()
                )
                auth_value.set_access_token(
                    keyList[2].strip(), keyList[3].strip()
                )
                return auth_value
            except IOError:
                print 'Failed file open'

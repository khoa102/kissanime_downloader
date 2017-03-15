#!/usr/bin/python
#
# episode.py - An object for storing information about an episode in kissanime
# Author: Khoa Tran

__version__ ='0.1'
__author__ = 'Khoa Tran'

class episode():
    def __init__(self):
        # Hide the value and expose them through property
        self._name = None
        self._URL = None
        self._downloadLinks = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = newName

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, newURL):
        self._URL = newURL

    @property
    def downloadLinks(self):
        return self._downloadLinks

    def setDownloadLink(self, quality, link):
        self._downloadLinks.setdefault(quality, link)



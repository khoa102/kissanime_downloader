#!/usr/bin/env python

import cfscrape
from lxml import html
import base64
import requests
import sys
from collections import OrderedDict
from subprocess import call
from episode import episode

class Kissanime():   
    def __init__(self):
        self.scraper = cfscrape.create_scraper(js_engine="Node")
        self.EPISODES_PREFIX = 'https://kissanime.ru'
        self.episodesName = None; # Storing the name of the episode
        self.episodes = []; # Storing the episode URL of the episodes
        
    def loadMenuPage(self,url):
        page = self.scraper.get(url.strip())
        tree = html.fromstring(page.content)
        episodes = tree.xpath('//table[@class="listing"]/tr/td//@href')
        episodesName = tree.xpath('//table[@class="listing"]/tr/td/a/text()')
        episodesName = [x.strip() for x in episodesName]
        for i in range(0, len(episodesName)):
        	temp = episode()
        	temp.name = episodesName[i]
        	temp.URL = self.EPISODES_PREFIX + episodes[i]
        	self.episodes.append(temp)

    def loadEpisodePage(self, num):
        page = self.scraper.get(self.episodes[num].URL)
        tree = html.fromstring(page.content)
        links = tree.xpath('//select[@id="slcQualix"]/option//@value')
        quality = tree.xpath('//select[@id="slcQualix"]/option/text()')
        videoLink = [base64.b64decode(x)for x in links]
        self.videoDict = OrderedDict(zip(quality,videoLink))
        for i in range(0, len(quality)):
        	self.episodes[num].setDownloadLink(quality[i], videoLink[i])
        

    def getEpisodesName(self):
        episodesName = [self.episodes[x].name for x in range (0, len(self.episodes))]
        return episodesName

    def getEpisodeURL(self, episodeNum):
        episodeURL = self.episodes[episodeNum].URL
        return episodeURL

    def getEpisodeQuality(self):
        self.quality = self.videoDict.keys()
        print self.quality
        return self.quality

    def getDownloadLink(self, qualityNum):
        quality = self.quality[qualityNum]
        downloadLink = self.videoDict[quality]
        return downloadLink

    def download(self, name, url):
        with open(name, 'wb') as video:
            response = requests.get(url, stream = True)
            totalLength = response.headers.get('content-length')

            if totalLength is None:
                video.write(response.content)
            else:
                dl = 0
                totalLength = int(totalLength)
                for data in response.iter_content(1024*1024):
                    dl += len(data)
                    video.write(data)
                    done = int(50* dl/totalLength)
                    percentage = int(100 * dl/totalLength)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) + str(percentage) + '%')
                    sys.stdout.flush()
        print            

def main():
    # Declare variable for the program
    url = None            # Store the url of the menu page
    episodeDict = None    # Store the dictionary of episode name and link
    name = None           # Store the name of all the episodes
    episodes = None       # Store the chosen episodes
    episodeURL = None     # Store the link of the chosen episodes
    videoDict = None      # Store the dictionary for chosen episode quality and link
    quality = None        # Store all the quality of the chosen episode
    chosenQuality = None  # Store the chosen quality
    option = None         # Store the download option
    episodeDownloaded = None # Store the number of episodes downloaded
    downloadLink = None   # Store the link for download 
    kissanime = Kissanime()

    ### (Check) Update cfsrape in shell
    call("pip install cfscrape --upgrade",shell = True)
    call("clear", shell = True)
    
    # Welcoming message
    print ("Hello guys, this is a program to download anime from kissanime")
    print ("Please input the url for the main page of your anime: ")
    url = raw_input()
    print;

    # Load the url into the kissanime object
    kissanime.loadMenuPage(url)
    
    # Retrieve the list of names of episode
    print " Here is a list of episodes for this anime: "
    name = kissanime.getEpisodesName()
    for i in range(0,len(name)):
        print str(i) + '. ' + name[i]
    print;
    
    # Show options
    print "What do you want to do?"
    print "  1. Download 1 episode"
    print "  2. Download multiple episodes"
    print "  3. Download all episodes"
    print "  4. Exit program"

    while(option != 4):
        # Choose option
        print "Please give your option:"
        option = int(raw_input())

        while(type(option) != int):
            print "Please give your option:"
            option = int(raw_input())
            print;

        # Option handling
        if option == 1:
            pass
            # Choose an episode
            print "Choose one of episode above (input the integer number): "
            episode = int(raw_input())
            while ((episode < 0) or (episode >= len(name)) or (type(episode) != int)):
                print "Wrong choice! Please give a valid episode number:"
                episode = int(raw_input())
            episodeURL = kissanime.getEpisodeURL(episode)
            print "You chose " + name[episode]
            print
            
            # Retrieve the list (dictionary) of quality
            kissanime.loadEpisodePage(episode)
            quality = kissanime.getEpisodeQuality()
            print "Choose one of the quality below (input the integer number): "
            for i in range(0,len(quality)):
                print str(i) + ". " + quality[i]
            
            # Choose a quality
            chosenQuality = int(raw_input())
            while ((chosenQuality < 0) or (chosenQuality>=len(quality)) or (type(chosenQuality) != int)):
                print "Wrong choice! Please give a valide quality choice: "
                chosenQuality = int(raw_input())
            downloadLink = kissanime.getDownloadLink(chosenQuality)
            print "You chose " + quality[chosenQuality]
            
            # Download the episode
            print "Currently Downloading " + name[episode] +": "
            kissanime.download(name[episode] + ".mp4",downloadLink)
        elif option == 2:
            episodeNum = []
            downloadLink = []
            downloadedName = []
            
            # Number of episodes downloaded?
            print "How many episodes do you want to download? "
            episodeDownloaded = int(raw_input())
            while ((episodeDownloaded <0) or (episodeDownloaded >= len(name)) or (type(episodeDownloaded) != int)):
                print "Please give a valid number of episode"
                episodeDownloaded = int(raw_input())
            
            # Make a list of name of the chosen episodes
            print "Choose one of episode above (input the integer number): "
            for i in range(0,episodeDownloaded):
                print "Your " + str(i) + " choice: "
                episode = int(raw_input())
                while ((episode < 0) or (episode >= len(name)) or (type(episode) != int)):
                    print "Wrong choice! Please give a valid episode number:"
                    episode = int(raw_input())
                episodeNum.append(episode)
                downloadedName.append(name[episode])
            print;
            
            # Retrieve the list (dictionary) of quality
            kissanime.loadEpisodePage(episodeNum[0])
            quality = kissanime.getEpisodeQuality()
            print "Choose one of the quality below (input the integer number): "
            for i in range(0,len(quality)):
                print str(i) + ". " + quality[i]

            # Choose a quality
            chosenQuality = int(raw_input())
            while ((chosenQuality < 0) or (chosenQuality>=len(quality)) or (type(chosenQuality) != int)):
                print "Wrong choice! Please give a valide quality choice: "
                chosenQuality = int(raw_input())
                
            for i in range(0, episodeDownloaded):
                kissanime.loadEpisodePage(episodeNum[i])
                downloadLink.append(kissanime.getDownloadLink(chosenQuality))
            print;

            # Download all the chosen episode with the chosen quality
            for i in range(0,episodeDownloaded):
                print "Currently Downloading " + str(downloadedName[i]) +": "
                kissanime.download(downloadedName[i] + ".mp4",downloadLink[i])
        elif option == 3:
            episodeNum = []
            downloadLink = []

            
            for i in range(0,len(name)):
                episodeNum.append(i)

            # Check to see if the code works
            #print episodeURL
            
            # Retrieve the list (dictionary) of quality
            kissanime.loadEpisodePage(episodeNum[0])
            quality = kissanime.getEpisodeQuality()
            print "Choose one of the quality below (input the integer number): "
            for i in range(0,len(quality)):
                print str(i) + ". " + quality[i]
                
            # Choose a quality
            chosenQuality = int(raw_input())
            while ((chosenQuality < 0) or (chosenQuality>=len(quality)) or (type(chosenQuality) != int)):
                print "Wrong choice! Please give a valide quality choice: "
                chosenQuality = int(raw_input())
                
            for i in range(0, len(name)):
                kissanime.loadEpisodePage(episodeNum[i])
                downloadLink.append(kissanime.getDownloadLink(chosenQuality))
                
            # Download all the episode with cosen quality
            for i in range(0,len(name)):
                print "Currently Downloading " + str(name[i]) + ": "
                kissanime.download(name[i] + ".mp4", downloadLink[i])
                
        elif option == 4:
            break
        else:
            pass
            # Print and ask for option again
    
    
if __name__ == '__main__':
    main()

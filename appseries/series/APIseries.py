from xml.etree import ElementTree as ET
from lxml import objectify
import requests
import sys

class APIseries:


	def __init__ (self):
		self.APIKEY = "EB224CCBC0C8E52F"

	def getTextValue(self, node):
		if node:
			return node.text
		else:
			return None

	def getStructuredSeries(self, name):
		resp = requests.get("http://www.thetvdb.com/api/GetSeries.php?seriesname="+name+"&language=es")
		if resp.status_code == 200:
			series = []
			root = objectify.fromstring(resp.content)
			for s in root.iterchildren():
				title = self.getTextValue(s.find("SeriesName"))
				banner = self.getTextValue(s.find("banner"))
				if not banner:
					banner = "https://i.imgur.com/VMLDXzQ.jpg" # Not available banner
				else:
					banner = "https://thetvdb.com/banners/" + banner
				overview = self.getTextValue(s.find("Overview"))
				apiId = self.getTextValue(s.find("seriesid"))
				series.append((title, banner, overview, apiId))
			return series

		else:
			return None
			
	def getDictSerie(self, ID):
		resp = requests.get("http://www.thetvdb.com/api/"+self.APIKEY+"/series/"+ID+"/es.xml")
		if resp.status_code == 200:
			root = objectify.fromstring(resp.content)
			serie = {}
			for s in root.iterchildren():
				serie['title'] = self.getTextValue(s.find("SeriesName"))
				banner = self.getTextValue(s.find("banner"))
				if not banner:
					serie['banner'] = "https://i.imgur.com/VMLDXzQ.jpg" # Not available banner
				else:
					serie['banner'] = "https://thetvdb.com/banners/" + banner
				serie['overview'] = self.getTextValue(s.find("Overview"))
				serie['apiId'] = ID
				
				airsday = self.getTextValue(s.find("Airs_DayOfWeek"))
				if not airsday:
					serie['Airs_DayOfWeek'] = 'None'
				else:
					serie['Airs_DayOfWeek'] = airsday	

				serie['genre'] = self.getTextValue(s.find("Genre"))
				serie['status'] = self.getTextValue(s.find("Status"))
				
			return serie

		else:
			return None

	def getSeries(self, name):

		response = requests.get("http://www.thetvdb.com/api/GetSeries.php?seriesname="+name+"&language=es")

		if (response.status_code == 200):
			data = ET.fromstring(response.content)
			return data

	def getSeriesByRemoteID(self, ID):

		response = requests.get("http://www.thetvdb.com/api/"+self.APIKEY+"/series/"+ID+"/es.xml")

		if (response.status_code == 200):
			data = ET.fromstring(response.content)
			return data

	def getEpisodes(self, ID):

		response = requests.get("http://www.thetvdb.com/api/"+self.APIKEY+"/series/"+ID+"/all/es.xml")

		if (response.status_code == 200):
			data = ET.fromstring(response.content)
			return data
			
	def getStructuredEpisodes(self, ID):
		resp = requests.get("http://www.thetvdb.com/api/"+self.APIKEY+"/series/"+ID+"/all/es.xml")
		if resp.status_code == 200:
			episodes = []
			root = objectify.fromstring(resp.content)
			for e in root.iterchildren():
				title = self.getTextValue(e.find("EpisodeName"))
				season = self.getTextValue(e.find("SeasonNumber"))
				number = self.getTextValue(e.find("EpisodeNumber"))
				
				# Siempre hay capitulos que les falta alguno de los datos
				if not title:
					title = 'No title'
				if not season:
					season = 9999
				if not number:
					number = 9999
					
				episodes.append((title, season, number))
			return episodes

		else:
			return None



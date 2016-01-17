#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import gzip
import urllib
import urllib2
import httplib
from StringIO import StringIO
from bs4 import BeautifulSoup

import json_util as jutil

import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class ShopURLCollector:

	''' public '''

	#def __init__(self, base_url):	
	#	self.base_url = base_url

	def set_city(self, city):

		self.city = city
	
	def set_food(self, food):
		
		self.food = food

	def extract_shop_urls(self):
			
		shop_urls = []

		page_i = 1
		while True:
			# fatch one dynamic page under this foods
			url  = "http://"+self.city+".meituan.com/category/"+self.food+"/all/page" + str(page_i)
			print "page %d:" % page_i
			try:
				html = self.__fatch_one_dynamic_page(url)
			except Exception as e:
				page_i += 1
				print "Exception: " + str(e)
				continue
			   	
			# get all preferentials in this dynamic page
			shop_urls.extend( self.__extract_shop_urls(html) )

			if html.find("下一页") < 0:
				break
			page_i += 1

		return shop_urls

	''' private '''

	def __fatch_one_dynamic_page(self, url):
		try:
			html1 = urllib2.urlopen(url).read()
		except:
			raise
		soup = BeautifulSoup(html1)
		
		item = soup.find("div", attrs={"class":"J-scrollloader cf J-hub"})
		json_str = item["data-async-params"]
		
		json_obj = json.loads(json_str)
		json_obj_data = json.loads(json_obj["data"])
		json_obj_data = jutil.byteify(json_obj_data)
		
		poiidList = json_obj_data["poiidList"]
		poiData   = json_obj_data["poiData"]
		bigImageMode = json_obj_data["bigImageMode"]
		
		if len(poiidList) > 32:
			# firstly we should get the list of shops which need dynamic loading
			# secondly we need do url encoding
			end_pos = len(poiidList)
			dict_poiidList = {}
			dict_bigImageMode = {}
			dict_poiData   = {}
			dict_poiidList["poiidList"] = poiidList[32:end_pos]
			dict_poiData["poiData"] = poiData[32:end_pos]
			dict_bigImageMode["bigImageMode"] = bigImageMode
		
			encode_poiidList = urllib.urlencode(dict_poiidList)
			encode_bigImageMode = urllib.urlencode(dict_bigImageMode)
			encode_poiData = urllib.urlencode(dict_poiData)
		
			encode_poiidList = encode_poiidList.replace("+", "")
			encode_bigImageMode = encode_bigImageMode.replace("True", "true")
			encode_poiData = encode_poiData.replace("+", "").replace("%27", "%22")
		
			post_data = encode_poiidList + "&" + encode_bigImageMode + "&" + encode_poiData
		
			# firstly we should do http post request
			# secondly we need splice static html and dynamic html to an entire html, and return it
			try:
				headers = {}
				headers["Accept-Encoding"] 	= "gzip, deflate"
				headers["Content-Type"] 	= "application/x-www-form-urlencoded; charset=UTF-8"
				headers["Host"]				= "sz.meituan.com"
				headers["X-Requested-With"]	= "XMLHttpRequest"
				headers["Content-Length"] 	= len(post_data)

				http_client = httplib.HTTPConnection("36.110.144.87", 80)
				http_client.request("POST", "/index/poilist", post_data, headers)

				response = http_client.getresponse()
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				json_str = f.read()

				html2 = json.loads(json_str)["data"]

				html1 = html1.replace("</body>", "").replace("</html>", "")
				html = html1 + "\n" + html2
				html += "</body>\n</html>\n"
				return html
			except:
				raise
			finally:
				if http_client:
					http_client.close()	
		else:
			# there is no need to do dynamic loading
			return html1

	def __extract_shop_urls(self, html):
		
		soup = BeautifulSoup(html)
		items = soup.find_all("a", attrs={"class":"link f3"})

		urls = []
		for item in items:
			urls.append(item["href"])
		return urls



if __name__ == "__main__":

	foods = Foods("http://sz.meituan.com/category/xican")

	urls = foods.extract_shop_urls()
	print urls

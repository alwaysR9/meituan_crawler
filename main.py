import os

from src.meituanShopURLCollector import ShopURLCollector
from src.webPageCollector import WebPageCollector

if __name__ == "__main__":

	# load urls
	print "Load URLs of Shops"
	url_collector = ShopURLCollector()
	url_collector.set_city("sz")
	url_collector.set_food("huoguo")
	shop_urls = url_collector.extract_shop_urls()
	print "The Number Of URL: %d" % len(shop_urls)

	# crawling
	print "Start To Crawling"
	crawler = WebPageCollector(is_debug=True)
	crawler.set_urls(shop_urls)
	crawler.start()

	# receive server data
	os.system("rm -r data")
	os.system("mkdir data")

	i = 1
	while True:
		
		item = crawler.pop()
		if item == None:
			break

		(url, data) = item
		with open("./data/"+str(i), "wb") as fo:
			fo.write(data)

		print "Receive " + str(i)
		i += 1

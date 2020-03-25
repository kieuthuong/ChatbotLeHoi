import scrapy 
import os
from lehoi.items import LehoiItem


class QuotesSpider(scrapy.Spider):
	name = "test1"
	start_urls=[ #dia chi bat dau cho spider
		'https://vi.wikipedia.org/wiki/L%E1%BB%85_h%E1%BB%99i_Vi%E1%BB%87t_Nam'
	]
	#Kiem tra trung bai viet
	# path =  "C:/Users/admin/Downloads/GR2/scrapy/lehoi/Data1"
	# listFile = os.listdir(os.path.expanduser(path))
	# print(len(listFile))

	def parse(self, response):
		festivals= response.xpath('//*[@id="mw-content-text"]/div/table[5]/tbody/tr')
		for festival in festivals[2:]:
			link = "https://vi.wikipedia.org" + festival.xpath('string(td[3]/a/@href)').extract_first()
			if link is not None:
				yield scrapy.Request(link, callback=self.saveFile)
	def saveFile(self, response):
		name = response.xpath('//*[@id="firstHeading"]/text()').extract()
		content = response.xpath('string(//*[@id="mw-content-text"]/div)').extract()
		
		if content is not None:
			strName = ''.join(name)
			strContent = '|'.join(content)
			path =  "C:/Users/admin/Downloads/GR2/scrapy/lehoi/Data12"
			listFile = os.listdir(os.path.expanduser(path))
			
			nameFile = strName+'.txt'
			text = strContent.replace('\n','').replace('|','').encode('utf-8')
			if nameFile not in listFile:
				f = open('Data12/'+nameFile,'wb')
				f.write(text)
				f.close()
			
				
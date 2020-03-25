import scrapy 
from lehoi.items import LehoiItem
class QuotesSpider(scrapy.Spider):
	name = "test2"
	start_urls=[
		'https://loca.vn/le-hoi/'
	]
	def parse(self, response):
		festivals= response.xpath('//*[@id="toc_container"]/ul/li/ul/li/a/@href').extract()
		for link in festivals[2:]:
			yield scrapy.Request('https://loca.vn/le-hoi/'+link, callback=self.saveFile)
		
	def saveFile(self,response):
		name = response.xpath('//*[@id="toc_container"]/ul/li[2]/ul/li[1]/a/text()').extract()
		print(name)
		content = response.xpath('/html/body/div[1]/div[3]/div[1]/section/article[1]/div/p[5]/text()').extract()
		
		print(content)
		# if content is not None:
		# 	strName = ''.join(name)
		# 	strContent = '|'.join(content)

		# 	nameFile = strName+'.txt'
		# 	text = strContent.replace('\n','').replace('|','').encode('utf-8')
		# 	f = open('Data/'+nameFile,'wb')
		# 	f.write(text)
		# 	f.close()
				
		# 	 ''.join(response.xpath('//*[@id]/text()').extract()).strip()
		# 	  ''.join(response.xpath('//*[@id]/text()').extract()).strip()
		# 	  //*[@id="2_Le_hoi_cau_an_ban_Muong"]
		# 	  //*[@id="toc_container"]/ul/li[2]/ul/li[2]/a
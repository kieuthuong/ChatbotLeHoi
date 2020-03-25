import scrapy 
from lehoi.items import LehoiItem
class QuotesSpider(scrapy.Spider):
	name = "test"
	start_urls=[
		'https://vi.wikipedia.org/wiki/Th%E1%BB%83_lo%E1%BA%A1i:L%E1%BB%85_h%E1%BB%99i_Vi%E1%BB%87t_Nam'
	]
	def parse(self, response):
		festivals= response.xpath('//*[@id="mw-pages"]/div/div/div/ul/li/a/@href').extract()
		for link in festivals:
			yield scrapy.Request('https://vi.wikipedia.org'+link, callback=self.saveFile)
	def saveFile(self,response):
		name = response.xpath('//*[@id="firstHeading"]/text()').extract()
		content = response.xpath('string(//*[@id="mw-content-text"]/div)').extract()
		if content is not None:
			strName = ''.join(name)
			strContent = '|'.join(content)

			nameFile = strName+'.txt'
			text = strContent.replace('\n','').replace('|','').encode('utf-8')
			f = open('Data/'+nameFile,'wb')
			f.write(text)
			f.close()
				
			
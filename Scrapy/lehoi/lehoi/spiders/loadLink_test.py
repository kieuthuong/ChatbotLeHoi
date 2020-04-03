import scrapy 
from lehoi.items import LehoiItem
class QuotesSpider(scrapy.Spider):
	name = "loadLinkWiki1"
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
		link = response.url.encode("utf-8")
		strName = ''.join(name)
		nameFile = 'linkLeHoiWiki.txt'
		f = open(nameFile,'ab+')
		f.write(strName.encode('utf-8'))
		f.write('\t'.encode('utf-8'))
		f.write(link)
		f.write('\n'.encode('utf-8'))
		f.close()
				
			
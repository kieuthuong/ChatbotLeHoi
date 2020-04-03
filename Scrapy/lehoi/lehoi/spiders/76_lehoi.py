import scrapy 
from lehoi.items import LehoiItem
class QuotesSpider(scrapy.Spider):
	name = "76lehoi"
	start_urls=[
		'https://www.maxreading.com/sach-hay/le-hoi-truyen-thong.html'
	]
	def parse(self, response):
		festivals= response.xpath('//*[@id="content"]/div/div[1]/div/table/tbody/tr/td[2]/a/@href').extract()
		for link in festivals:
			yield scrapy.Request(link.replace('..', 'https://www.maxreading.com'), callback=self.saveFile)
	def saveFile(self,response):
		name = response.xpath('//*[@id="content"]/div/div[1]/div/h3/text()').extract()
		content = response.xpath('string(//*[@id="chapter"]/div)').extract()
		# if content is not None:
		strName = ''.join(name)
		strContent = '|'.join(content)
		nameFile = strName.lstrip()+'.txt'
		text = strContent.replace('\n','').replace('|','').encode('utf-8')
		link = response.url.encode("utf-8")
		f = open('76lehoi_maxreading/'+nameFile,'wb')
		f.write(text)
		f.close()
		#ghi link cac le hoi
		# nameFileLink = 'link76Lehoi.txt'
		# f = open(nameFileLink,'ab+')
		# f.write(strName.encode('utf-8'))
		# f.write('\t'.encode('utf-8'))
		# f.write(link)
		# f.write('\n'.encode('utf-8'))
		# f.close()
				
			
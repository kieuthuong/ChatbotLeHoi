import scrapy 
from lehoi.items import LehoiItem
class QuotesSpider(scrapy.Spider):
	name = "lehoi"
	start_urls=[ #dia chi bat dau cho spider
		'https://vi.wikipedia.org/wiki/L%E1%BB%85_h%E1%BB%99i_Vi%E1%BB%87t_Nam'
	]
	def parse(self, response):
		festivals= response.xpath('//*[@id="mw-content-text"]/div/table[5]/tbody/tr')
		# ignore the table header row
		for festival in festivals[2:]:
			viTri = festival.xpath('string(td[2])').extract_first()
			tenLeHoi = festival.xpath('string(td[3])').extract_first()
			lanDauToChuc = festival.xpath('string(td[4])').extract_first()
			ghiChu = festival.xpath('string(td[5])').extract_first()
			link = "https://vi.wikipedia.org" + festival.xpath('string(td[3]/a/@href)').extract_first()
			

			print("Vi Tri :" + viTri)
			print("Ten Le Hoi"+tenLeHoi)
			print("Lan Dau To Chuc"+lanDauToChuc)
			print("Ghi Chu"+ghiChu)
			print("link"+link)
			# if link is not None:
			# 	yield scrapy.Request(link, callback=self.saveFile)
			# else:
			# 	continue 
			if link is not None:
				yield scrapy.Request(link, callback=self.saveFile)
			else:
				continue

	def saveFile(self, response):
		noiDung = response.xpath('string(//*[@id="mw-content-text"]/div/p[1])').extract_first()
		if noiDung is not None:
			print("THUONG6"+noiDung)
				
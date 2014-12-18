import scrapy
from datetime import datetime
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Plosone.items import pubMetaItem, pubMNMItem, pubFigureItem
from scin.models import pub_meta

class PlosoneSpider(CrawlSpider):
    name = "Plosone"
    allowed_domains = ["plosone.com", "plosone.org"]
    start_urls = [
		#'http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0061362'		# TODO: input parameter #2
		#'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
		'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
    ]
    # single page: 'http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0061362'
	# single page2: 'http://www.plosone.org/article/info:doi%2F10.1371%2Fjournal.pone.0054089'
    # 20130101 to 20130110: 'http://www.plosone.org/search/advanced?pageSize=15&sort=&queryField=publication_date&startDateAsString=2013-01-01&endDateAsString=2013-01-10&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2013-01-10T23%3A59%3A59Z]+&journalOpt=some&filterJournals=PLoSONE&subjectCatOpt=all&filterArticleTypesOpt=all'
    # 2013 year: 'http://www.plosone.org/search/advanced?searchName=&weekly=&monthly=&startPage=0&pageSize=60&filterKeyword=&resultView=&unformattedQuery=publication_date%3A[2013-01-01T00%3A00%3A00Z+TO+2014-01-01T23%3A59%3A59Z]&sort=Relevance&filterStartDate=&filterEndDate=&filterJournals=PLoSONE'
    
    rules = (
        ###===RULES FOR NEXT PAGE LINK===
        # allow: allows certain link url patterns to be followed.
        # restricted_xpaths: xpath for the next button to follow.
        Rule (SgmlLinkExtractor(allow=(".+", ), ###
              restrict_xpaths=(
              "//div[@class='pagination']/a[@class='next']",) ###
              ), follow=True),
		
        ###===RULES FOR AD PAGE LINK===
        # allow: link patterns for ads to click
        # callback: function name for processing ad page after visiting it
        # restricted_xpaths: xpaths under which the links are located.
        Rule (SgmlLinkExtractor(allow=(".*/article/.+", ), deny=(".*/search/.+"), # ext saccurent
             restrict_xpaths=(
             "//div[@class='main']/ul[@id='search-results']//span[@class='article']/a")
             ),
             callback="parse_item", follow=False),
    )
    counter = 0;
		
    def parse_item(self, response):
		docHeader = self.parseHeader(response)
		self.parseMNM(response, docHeader)
		self.parseFigure(response, docHeader)
		
		self.counter += 1;
		url_name = response.url
		print "[RESULT] scrap paper #%d" % self.counter
		print "[RESULT] url=%s" % url_name
        #documentId = self.parseHeader(response)
        #self.parseMNM(response, documentId)
		
    def parseHeader(self, response):
		publisher = "Plos One"				# TODO: input parameter #1
		src_address = response.url			# self.start_urls[0]
		pdf_address = response.xpath("//div[@class='download']//a/@href").extract()
		title = response.xpath("string(//h1)").extract()
				
		doc_id = ""
		editors = ""
		pub_date = ""
		copyright = ""
		data_availibility = ""
		funding = ""
		competing_interest = ""
		
		infoList = response.xpath("//div[@class='articleinfo']/p")
		for infoContent in infoList:
			content = infoContent.xpath("string()").re(r"(?<=doi:).*")
			if len(content) > 0:
				doc_id = content
			content = infoContent.xpath("string()").re(r"(?<=Editor: ).*\n*.*")
			if len(content) > 0:
				editors = content
			content = infoContent.xpath("string()").re(r"(?<=Published: )[A-Za-z]+ [0-9]+, [0-9]+")
			if len(content) > 0:
				pub_date = content
			content = infoContent.xpath("string()").re(r"(?<=Copyright: ).*")
			if len(content) > 0:
				copyright = content
			content = infoContent.xpath("string()").re(r"(?<=Data Availability: ).*")
			if len(content) > 0:
				data_availibility = content
			content = infoContent.xpath("string()").re(r"(?<=Funding: ).*")
			if len(content) > 0:
				funding = content
			content = infoContent.xpath("string()").re(r"(?<=Competing interests: ).*")
			if len(content) > 0:
				competing_interest = content
		
		rec_update_time = datetime.now()
		rec_update_by = "sys"
		
		# debug messages
		#print "publisher = %s" % publisher
		#print "src_address = %s" % src_address
		#print "pdf_address = %s" % pdf_address
		#print "doc_id = %s" % doc_id
		#print "title = %s" % title
		#print "editors = %s" % editors
		#print "pub_date = %s" % pub_date
		#print "copyright = %s" % copyright
		#print "data_availibility = %s" % data_availibility
		#print "funding = %s" % funding
		#print "competing_interest = %s" % competing_interest
        
		# write to database
		item = pubMetaItem()
		item['publisher'] = publisher
		if len(pdf_address) > 0:
			item['pdf_address'] = pdf_address[0]
		item['src_address'] = src_address
		item['doc_id'] = doc_id[0]
		item['title'] = title[0]
		item['editors'] = editors[0]
		item['pub_date'] = datetime.strptime(pub_date[0], '%B %d, %Y')			# convert to djan
		if len(copyright) > 0:
			item['copyright'] = copyright[0]
		if len(data_availibility) > 0:
			item['data_availibility'] = data_availibility[0]
		if len(funding) > 0:
			item['funding'] = funding[0]
		if len(competing_interest) > 0:
			item['competing_interest'] = competing_interest[0]
		item['rec_update_time'] = datetime.now()			# TODO: use GMT instead
		item['rec_update_by'] = "sys"
		docHeader = item.save()
		
		return docHeader

    def parseMNM(self, response, docHeader):
		headerList = response.xpath("//div[contains(@id,'section')]/h3/text()").extract()
		
		# find section id having title "Materials and Methods"
		mnmHeaderNb = 1
		for header in headerList:
			if header == "Materials and Methods" or header == "Methods":
				break
			mnmHeaderNb = mnmHeaderNb + 1
		
		# assign M&M section selector
		mnmSelectorStr = "//div[@id='section%d']" % mnmHeaderNb
		mnmSelector = response.xpath(mnmSelectorStr)
		
		subHeaderListStr = "//div[@id='section%d']/h4/text()" % mnmHeaderNb
		subHeaderList = mnmSelector.xpath(subHeaderListStr).extract()
		if len(subHeaderList) > 0:
			headerSeq = 1
			for subHeader in subHeaderList:
				#subHeaderStr = "//h4[%d]" % headerSeq
				subHeaderStr = "//div[@id='section%d']/h4[%d]" % (mnmHeaderNb, headerSeq)
				for h4 in mnmSelector.xpath(subHeaderStr):
					paragraphs = h4.xpath("""set:difference(./following-sibling::p,
													./following-sibling::h4[1]/following-sibling::p)""").extract()
					contentSeq = 1
					for prgrph in paragraphs:
						item = pubMNMItem()
						item['doc_id'] = docHeader
						item['section_id'] = headerSeq
						item['header'] = subHeader
						item['content_seq'] = contentSeq
						item['content'] = prgrph
						item.save()
						contentSeq = contentSeq + 1
				headerSeq = headerSeq + 1
		else:
			for h3 in mnmSelector.xpath(header):
				paragraphs = h3.xpath("""set:difference(./following-sibling::p,
														./following-sibling::h3[1]/following-sibling::p)""").extract()
				contentSeq = 1
				for prgrph in paragraphs:
					item = pubMNMItem()
					item['doc_id'] = docHeader
					item['section_id'] = 1
					item['header'] = ""
					item['content_seq'] = contentSeq
					item['content'] = prgrph
					item.save()
					contentSeq = contentSeq + 1
		
		#for h4 in selector.xpath('//h4[1]'):
		#	paragraphs = h4.xpath("""set:difference(./following-sibling::p,
		#											./following-sibling::h4[1]/following-sibling::p)""").extract()
		#	print paragraphs
			
		# ensure mnm would not be the last section
		#if mnmHeaderNb < len(headerList):
		#	mnmSubHeaderStr = "//div[@id='section%d']/h4/text()" % mnmHeaderNb
		#	subHeaderList = response.xpath(mnmSubHeaderStr).extract()
		#	
		#	itemId = 1
		#	for subheader in subHeaderList:
		#		xpathContentStr = "//div[@id='section%d']/p[%d]/text()" % (mnmHeaderNb, itemId)
		#		item = pubMNMItem()
		#		item['doc_id'] = docHeader
		#		item['section_id'] = itemId
		#		item['header'] = subheader
		#		contentList = response.xpath(xpathContentStr).extract()
		#		if len(contentList) > 0:
		#			item['content'] = contentList[0]
		#		item.save()
		#		itemId += 1
			
    def parseFigure(self, response, docHeader):
		poiFullname = docHeader.doc_id
		poiNum = poiFullname[-7:]
		xpathFigHeaderList = "//div[contains(@id,'pone-%s-g00')]/p[1]" % poiNum
		
		#print "[DEBUG] figure xpathFigHeaderList: %s" % xpathFigHeaderList
		figHeaderList = response.xpath(xpathFigHeaderList).extract()
		
		itemId = 1
		for header in figHeaderList:
			xpathHeaderStr = "string(//div[contains(@id,'pone-%s-g00%d')]/p[1])" % (poiNum, itemId)
			xpathContentStr = "string(//div[contains(@id,'pone-%s-g00%d')]/p[2])" % (poiNum, itemId)
			xpathUrlStr = "string(//div[contains(@id,'pone-%s-g00%d')]//a/@href)" % (poiNum, itemId)
			#print xpathHeaderStr
			
			item = pubFigureItem()
			item['doc_id'] = docHeader
			item['figure_id'] = itemId
			headerList = response.xpath(xpathHeaderStr).extract()
			contentList = response.xpath(xpathContentStr).extract()
			urlList = response.xpath(xpathUrlStr).extract()
			if len(headerList) > 0:
				item['header'] = headerList[0]
			if len(contentList) > 0:
				item['content'] = contentList[0]
			if len(urlList) > 0:
				item['url'] = urlList[0]
			item.save()
			itemId = itemId + 1
				

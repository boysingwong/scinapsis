import codecs
import MySQLdb
import re
import sys
from warnings import filterwarnings

def search_product_tech(doc_id, supplier_id):
	filterwarnings('ignore', category = MySQLdb.Warning)
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	try:
		mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
		mysql_cursor = mysql.cursor()
		
		# call search protein keywords
		args = [doc_id, supplier_id]
		mysql_cursor.callproc( 'scin_db.pub_technique_product_exists_by_sup', args )
		
		query = ("SELECT figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content FROM scin_db.pub_tech_prod_temp")
		mysql_cursor.execute(query)
		
		rsltCount = 0
		for (figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content) in mysql_cursor:
		  outputStr = "result: %s, %s, %s, %d " % (tech_parental_name, tech_alternative, product_name, figure_id)
		  
		  #print "process figure#: %d " % figure_id
		  
		  sentenceList = re.split(ur'(?<!\w\.\w.)(?<![A-Z]\.)(?<=\.|\?)\s', content)
		  for sentence in sentenceList:
			technique_exists = False
			protein_exists = False
			
			#print "process sentence [%s]" % sentence

			# a. check tech_alternative exists
			pattern = ur'(?i)\b%s\b' % (tech_alternative)
			if re.search(pattern, sentence):
				#print "tech_alternative found [%s]" % tech_alternative
				technique_exists = True
			else:
				continue
			
			# b. check protein exists:
			sentence = sentence.replace("(", "")
			sentence = sentence.replace(")", "")
			wordList = re.split('\s|-', sentence)
			
			for word in wordList:
				if len(word) < 3:
					continue

				if word.lower() == product_name.lower():
					#print "product_name found exact match [%s]" % product_name
					protein_exists = True
				elif word in product_name:
					#print "product_name found exact partial match [%s]" % product_name
					protein_exists = True
				else:
					continue
					
			if technique_exists and protein_exists:
				insertStmt = ("INSERT INTO scin_db.pub_tech_prod_result "
							  "(doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, sentence) "
							  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
				mysql_cursor.execute(insertStmt, (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, sentence) )
				mysql.commit()
				rsltCount = rsltCount + 1

		mysql_cursor.close()
		mysql.close()
		
		return rsltCount

	except MySQLdb.Error, e:
		errmsg = "MySQL Error @run_product_tech (@%s) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
		with open("error.log", 'w') as w:
			w.write(errmsg)
		sys.exit(1)

import codecs
import MySQLdb
import re
import sys
from warnings import filterwarnings

def search_product_tech(doc_id):
	filterwarnings('ignore', category = MySQLdb.Warning)
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	try:
		mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
		mysql_cursor = mysql.cursor()
		
		# call search protein keywords
		args = [doc_id]
		mysql_cursor.callproc( 'scin_db.pub_technique_product_exists', args )
		
		query = ("SELECT pub_figure_id, tech_parental_name, tech_alternative, supplier_name, catalog_nb, product_name, content FROM scin_db.pub_tech_prod_temp")
		mysql_cursor.execute(query)
		
		rsltCount = 0
		for (pub_figure_id, tech_parental_name, tech_alternative, supplier_name, catalog_nb, product_name, content) in mysql_cursor:
		  outputStr = "result: %s, %s, %s, %d " % (tech_parental_name, tech_alternative, product_name, pub_figure_id)
		  
		  pat1 = ur'\b%s\b.*?\b%s\b' % (tech_alternative, product_name)
		  pat2 = ur'\b%s\b.*?\b%s\b' % (product_name, tech_alternative)
		  
		  sentenceList = re.split(ur'(?<!\w\.\w.)(?<![A-Z]\.)(?<=\.|\?)\s', content)
		  for sentence in sentenceList:
			 result1 = re.search(pat1, sentence)
			 result2 = re.search(pat2, sentence)
			 if result1 or result2:
				insertStmt = ("INSERT INTO scin_db.pub_tech_prod_result "
							  "(doc_id, pub_figure_id, tech_parental_name, tech_alternative, supplier_name, catalog_nb, product_name, sentence) "
							  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
				mysql_cursor.execute(insertStmt, (doc_id, pub_figure_id, tech_parental_name, tech_alternative, supplier_name, catalog_nb, product_name, sentence) )
				mysql.commit()
				rsltCount = rsltCount + 1

		mysql_cursor.close()
		mysql.close()
		
		return rsltCount

	except MySQLdb.Error, e:
		errmsg = "MySQL Error (@%s) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
		with open("error.log", 'w') as w:
			w.write(errmsg)
		sys.exit(1)

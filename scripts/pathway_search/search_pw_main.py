import sys
import MySQLdb
import codecs

import run_pw_action_word
import run_pw_protein
import run_pathway
import flush_pw_temp_tables

from warnings import filterwarnings

sys.setrecursionlimit(20000)
filterwarnings('ignore', category = MySQLdb.Warning)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
try:
	mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
	mysql_cursor = mysql.cursor()
	
	mysql_cursor.execute("SELECT id FROM scin_db.scin_pub_meta ht "
							"WHERE EXISTS ( "
							"SELECT 1 FROM scin_db.scin_pub_result rt "
							"WHERE ht.id = rt.doc_id_id "
							") "
							"AND id BETWEEN 1 and 2500 "
							"ORDER BY id")
	
	for (id) in mysql_cursor:
	  doc_id = id
	  print "procesing doc_id: %d" % doc_id
	  actionWordResult = run_pw_action_word.search_action_word(doc_id)
	  if actionWordResult > 0:
	    protResult = run_pw_protein.search_pw_protein(doc_id)
	    if protResult > 0:
		    run_pathway.search_pathway(doc_id)
	    flush_pw_temp_tables.flush_pw_temp_tables(doc_id)
	  print "doc_id [%d] search completed" % doc_id
	
	mysql_cursor.close()
	mysql.close()

except MySQLdb.Error, e:
	errmsg = "MySQL Error (@%d) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
	with open("error.log", 'w') as w:
		w.write(errmsg)
	sys.exit(1)

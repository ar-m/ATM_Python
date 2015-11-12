import MySQLdb
def verify_id(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT * FROM Users WHERE User_ID=%s AND User_PIN=%s")
	ux = (uid,pin)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	print f[0][2]
	cnx.commit()
	cursor.close()
	cnx.close()
	"""if len(f) != 0:
		return #
	else:
		return False"""

verify_id("1234","4321")
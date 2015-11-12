import MySQLdb

def num_of_accounts(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT Num_Of_Accounts FROM Users WHERE User_ID=%s AND User_PIN=%s")
	ux = (uid,pin)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	print f
	return f[0][0]

def increment_accounts(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("UPDATE Users SET Num_Of_Accounts=Num_Of_Accounts+1 WHERE User_ID=%s AND User_PIN=%s LIMIT 1;")
	ux = (uid,pin)
	print ux
	cursor.execute(query, ux)
	cnx.commit()
	cursor.close()
	cnx.close()
	print num_of_accounts(uid,pin)

increment_accounts("1337","1337")
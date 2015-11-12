import MySQLdb

def account_balance_print(uid):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT Account_Name,Balance FROM Accounts WHERE User_ID=%s AND User_ID!=%s")
	ux = (uid, "xxxx")
	cursor.execute(query, ux)
	x = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	h = 1
	for i in x:
		print ""
		print "[" + str(h) + "] Account: ", str(i[0])
		print "    Balance: ", i[1]
		h+=1

account_balance_print(1234)
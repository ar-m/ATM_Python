import MySQLdb

def money_in_account(uid,account):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT Balance FROM Accounts WHERE User_ID=%s AND Account_Name=%s")
	ux = (uid,account)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	return f[0][0]

def add_to_account(uid,account,amount):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	b = money_in_account(uid,account) + float(amount)
	query = ("UPDATE Accounts SET Balance=%s WHERE User_ID=%s AND Account_Name=%s")
	ux = (b,uid,account)
	cursor.execute(query, ux)
	cnx.commit()
	cursor.close()
	cnx.close()

add_to_account("1234","amine123","80")
import MySQLdb

def increment_accounts(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT Num_Of_Accounts,Full_Name FROM Users WHERE User_ID=%s AND User_PIN=%s")
	ux = (uid,pin)
	cursor.execute(query, ux)
	y = cursor.fetchall()[0][1]
	cursor.execute(query, ux)
	x = cursor.fetchall()[0][0]

	query = ("DELETE FROM Users WHERE User_ID=%s AND User_PIN=%s LIMIT 1")
	ux = (uid,pin)
	cursor.execute(query, ux)

	x += 1
	print x
	query = ("INSERT INTO Users (User_ID, User_PIN, Full_Name, Num_Of_Accounts) VALUES (%s, %s, %s, %s)")
	ux = (uid,pin,y,x)
	cursor.execute(query, ux)

increment_accounts("1889","0597")
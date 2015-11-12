import MySQLdb
def id_exists(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT * FROM Users WHERE User_ID=%s AND User_PIN=%s")
	ux = (uid,pin)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	if len(f) != 0:
		return True
	else:
		return False

def u_print(uid,pin):
	if id_exists(uid,pin):
		print "True"
	else:
		print "False"

u_print("1234","4321")
u_print("1337","3242")
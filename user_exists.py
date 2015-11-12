import MySQLdb
def user_exists(uid):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	cursor.execute("SELECT * FROM Users WHERE User_ID=%s AND User_PIN!=%s", (uid,"xxxx"))
	f = cursor.fetchall()
	if len(f) != 0:
		return True
	else:
		return False

def u_print(uid):
	if user_exists(uid):
		print "True"
	else:
		print "False"

u_print("1234")
u_print("1337")
import os

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

def new_account(uid,pin):
	os.system('clear')
	x = raw_input("Press x.\n\n")
	while x != 'x':
		os.system('clear')
		x = raw_input("Press x.\n\n")
	os.system('clear')
	account_name = raw_input("Write what you would like as your account name below. It can be anything, but remember it, because you will be using it for transfers.\n\n")
	#
	os.system('clear')
	x = raw_input("Your account was successfully created. Return 'x' to continue.\n\n")
	while x != 'x':
		os.system('clear')
		x = raw_input("Your account was successfully created. Return 'x' to continue.\n\n")

new_account("1337","1337")
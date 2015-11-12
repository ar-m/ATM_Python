import os
import time
import MySQLdb
import re

display = {
	'X': "----------------------------------------------------- START -------------------------------------------------------------------",
	'Y': "Thank you for using Amine's ATM. To navigate, type the options between the [] brackets into the editor.",
	'Z': "Type 'x', then press enter to continue.",
	'0': "[0] CLEAR DISPLAY\n[1] LOG IN\n[2] CREATE NEW USER\n[3] QUIT",
	'1': "USER CREATE:\n\nWelcome to User Create! Type 'x', then press enter to continue.",
	'2': "What is your Full Name? Type it below and press enter. Cannot be more than 45 characters.", 
	'3': "Choose a User ID: Must be four digits.",
	'4': "Choose a PIN: Must be four digits.",
	'5': "LOG IN - Type your User ID\n",
	'6': "LOG IN - Type your PIN number\n",
	'7': "Verifying Login...",
	'A': "[0] Log Off\n[1] New Account Create",
	'B': "[0] Log Off\n[1] New Account Create\n[2] Use An Account",
	'C': "What would you like to do?\n[0] Leave\n[1] Make a withdrawal.\n[2] Make a deposit\n[3] Make a transfer."
}
#go to a specific account
#display balance, withdraw, deposit transfer

last_fails = []
freeze_start = None

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

def deduct_from_account(uid,account,amount):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	b = money_in_account(uid,account) - float(amount)
	query = ("UPDATE Accounts SET Balance=%s WHERE User_ID=%s AND Account_Name=%s")
	ux = (b,uid,account)
	cursor.execute(query, ux)
	cnx.commit()
	cursor.close()
	cnx.close()

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

def withdraw(uid):
	print "WITHDRAWAL - Account Name"
	account_balance_print(uid)
	print "Type the name of the account you would like to withdraw from:"
	x = raw_input("\n")
	while (not account_exists(uid,x)):
		clear()
		print "WITHDRAWAL - Account Name"
		account_balance_print(uid)
		print "Type the name of the account you would like to withdraw from:\nAccount doesn't exist."
		x = raw_input("")
	clear()
	print "WITHDRAWAL - Amount"
	string = "Type the amount of money you would like to withdraw:\n(Maximimum $" + str(money_in_account(uid,x)) + ")\n\n"
	y = raw_input(string)
	z = re.match(r'^[0-9].*$', y)
	while (z==None or float(y)>money_in_account(uid,x)) and y!="q":
		clear()
		print "WITHDRAWAL - Amount"
		string = "Type the amount of money you would like to withdraw:\n(Maximimum $" + str(money_in_account(uid,x)) + ")\nNot a valid amount. (Return q to quit)\n"
		y = raw_input(string)
		z = re.match(r'^[0-9].*$', y)
	if y != "q":
		deduct_from_account(uid,x,y)
		wait("Withdrawal was successful.")

def deposit(uid):
	print "DEPOSIT - Account Name"
	account_balance_print(uid)
	print "Type the name of the account you would like to deposit to:"
	x = raw_input("\n")
	while (not account_exists(uid,x)):
		clear()
		print "DEPOSIT - Account Name"
		account_balance_print(uid)
		print "Type the name of the account you would like to deposit to:\nAccount doesn't exist."
		x = raw_input("")
	clear()
	print "DEPOSIT - Amount"
	string = "Type the amount of money you would like to deposit:\n\n\n"
	y = raw_input(string)
	z = re.match(r'^[0-9].*$', y)
	while (z==None) and y!="q":
		clear()
		print "DEPOSIT - Amount"
		string = "Type the amount of money you would like to deposit:\nOnly digits.\n(Return q to quit)\n"
		y = raw_input(string)
		z = re.match(r'^[0-9].*$', y)
	if y != "q":
		add_to_account(uid,x,y)
		wait("Deposit was successful.")


def transfer(uid):
	print "TRANSFER - FROM Account Name"
	account_balance_print(uid)
	print "Type the name of the account you would like to transfer FROM:"
	x1 = raw_input("\n")
	while (not account_exists(uid,x1)):
		clear()
		print "TRANSFER - FROM Account Name"
		account_balance_print(uid)
		print "Type the name of the account you would like to transfer FROM:\nAccount doesn't exist."
		x1 = raw_input("")

	print "\nTRANSFER - TO Account Name"
	account_balance_print(uid)
	print "Type the name of the account you would like to transfer TO:"
	x2 = raw_input("\n")
	while (not account_exists(uid,x2)):
		clear()
		print "TRANSFER - TO Account Name"
		account_balance_print(uid)
		print "Type the name of the account you would like to transfer TO:\nAccount doesn't exist."
		x2 = raw_input("")

	print "\nTRANFER - Amount"
	string = "Type the amount of money you would like to withdraw:\n(Maximimum $" + str(money_in_account(uid,x1)) + ")\n\n"
	y = raw_input(string)
	z = re.match(r'^[0-9].*$', y)
	while (z==None or float(y)>money_in_account(uid,x1)) and y!="q":
		clear()
		print "WITHDRAWAL - Amount"
		string = "Type the amount of money you would like to withdraw:\n(Maximimum $" + str(money_in_account(uid,x1)) + ")\nNot a valid amount. (Return q to quit)\n"
		y = raw_input(string)
		z = re.match(r'^[0-9].*$', y)

	if y != "q":
		deduct_from_account(uid,x1,y)
		add_to_account(uid,x2,y)
		wait("Deposit was successful.")

""" """
def use_account(uid,pin):
	y = None
	while y != '0':
		clear()
		path = 'C'
		pathx(path)
		y = raw_input("\n")
		if y == "1":
			clear()
			withdraw(uid)
		elif y == "2":
			clear()
			deposit(uid)
		elif y == "3":
			if num_of_accounts(uid,pin) == 1:
				wait("You cannot make a transfer with only one account.")
			else:
				clear()
				transfer(uid)
""" """

def num_of_accounts(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT Num_Of_Accounts FROM Users WHERE User_ID=%s AND User_PIN=%s")
	ux = (uid,pin)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	return f[0][0]

def increment_accounts(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("UPDATE Users SET Num_Of_Accounts=Num_Of_Accounts+1 WHERE User_ID=%s AND User_PIN=%s LIMIT 1;")
	ux = (uid,pin)
	cursor.execute(query, ux)
	cnx.commit()
	cursor.close()
	cnx.close()

def create_account(uid,account_name):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	add_user = "INSERT INTO Accounts (User_ID, Account_Name, Balance) VALUES (%s, %s, %s)"
	data_user = (uid, account_name, 0.00)
	cursor.execute(add_user,data_user)
	cnx.commit()
	cursor.close()
	cnx.close()

def account_exists(uid,account_name):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT * FROM Accounts WHERE User_ID=%s AND Account_Name=%s")
	ux = (uid,account_name)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	if len(f) != 0:
		return True
	else:
		return False

def new_account(uid,pin):
	clear()
	wait("NEW ACCOUNT CREATE")
	clear()
	account_name = raw_input("Write what you would like as your account name below.\nIt can be anything, but remember it, because you will be using it for transfers.\n\n")
	while account_exists(uid, account_name):
		clear()
		account_name = raw_input("Write what you would like as your account name below.\nIt can be anything, but remember it, because you will be using it for transfers.\nAnd account under that name already exists.\n")
	create_account(uid,account_name)
	clear()
	increment_accounts(uid,pin)
	x = raw_input("Your account was successfully created. Return 'x' to continue.\n\n")
	while x != 'x':
		clear()
		x = raw_input("Your account was successfully created. Return 'x' to continue.\n\n")

def is_frozen_and_should():
	global freeze_start
	if freeze_start == None:
		return False
	elif time.time() < freeze_start + 60:
		return True
	else:
		freeze_start = None
		return False

def freeze_or_dont():
	global last_fails
	l = len(last_fails)
	if l>2 and last_fails[l-3]>time.time()-60:
		return True
	else:
		return False

def freeze():
	global last_fails
	global freeze_start
	freeze_start = time.time()
	last_fails = []

def fail(now):
	global last_fails
	last_fails.append(now)
	if freeze_or_dont():
		freeze()

def insert_new_user(name, uid, pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	add_user = "INSERT INTO Users (User_ID, User_PIN, Full_Name, Num_Of_Accounts) VALUES (%s, %s, %s, %s)"
	data_user = (uid, pin, name, 0)
	cursor.execute(add_user,data_user)
	cnx.commit()
	cursor.close()
	cnx.close()

def verify_id(uid,pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	query = ("SELECT * FROM Users WHERE User_ID=%s AND User_PIN=%s")
	ux = (uid,pin)
	cursor.execute(query, ux)
	f = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	if len(f) != 0:
		return f[0][2]
	else:
		return False

def user_exists(uid):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	cursor.execute("SELECT * FROM Users WHERE User_ID=%s AND User_PIN!=%s", (uid,"xxxx"))
	f = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	if len(f) != 0:
		return True
	else:
		return False

def valid_name(namex):
	if len(namex) > 45 or len(namex) < 5:
		return False
	elif re.match(r'^[a-zA-Z][ A-Za-z]*$', namex) is None:
		return False
	else:
		return True

def valid_uid(numb):
	x = re.match(r'^[0-9]*$', numb)
	if len(numb) != 4:
		return "\nUID must be 4 digits."
	elif x is None:
		return "\nOnly digits, nothing else."
	elif user_exists(numb):
		return "\nUser ID already exists. Pick another one."
	else:
		return True

def valid_num(numb):
	x = re.match(r'^[0-9]*$', numb)
	if len(numb) != 4:
		return "\nPIN must be 4 digits."
	elif x is None:
		return "\nOnly digits, nothing else."
	else:
		return True

def pathx(x):
	print display[x]

def clear():
	os.system('clear');

def wait(text):
	clear()
	print text
	pathx('Z')
	while raw_input("\n")!="x":
		clear()
		print text
		pathx('Z')

#
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
	for i in x:
		print ""
		print "Account: ", str(i[0])
		print "Balance: ", i[1]

def accounts(uid,pin):
	y = "x"
	while y != "0":
		if num_of_accounts(uid,pin) == 0:
			path = 'A'
		else:
			path = 'B'
		clear()
		pathx(path)
		y = raw_input(">> acc$ ")
		if y == "1":
			clear()
			new_account(uid,pin)
		elif y == "2":
			if path == 'A':
				pass
			elif path == 'B':
				use_account(uid,pin)
#

def login():
	global last_fails
	global freeze_start
	if is_frozen_and_should():
		remaining = str(60 - (time.time() - freeze_start))
		x = "The screen is frozen because of too many failed login attempts. " + str(remaining) + " seconds remaining."
		wait(x)
	else:
		path = '5'
		clear()
		pathx(path)
		uid = raw_input("UID: ")
		path = '6'
		clear()
		pathx(path)
		pin = raw_input("PIN: ")
		path = '7'
		clear()
		pathx(path)
		nameq = verify_id(uid,pin)
		if nameq:
			string = "Welcome " + nameq + "!\n"
			wait(string)
			accounts(uid,pin)
		else:
			wait("Fail.")
			fail(time.time())

def create_user():
	path = '1'
	clear()
	pathx(path)
	while raw_input("\n")!="x":
		clear()
		pathx(path)
	clear()
	path = '2'
	pathx(path)
	name = raw_input("\n")
	while valid_name(name)!=True:
		clear()
		print display[path] + "\nThat wasn't valid."
		name = raw_input("")
	clear()
	path = '3'
	pathx(path)
	uid = raw_input("\n")
	while valid_uid(uid)!=True:
		clear()
		print display[path] + valid_uid(uid)
		uid = raw_input("")
	clear()
	path = '4'
	pathx(path)
	pin = raw_input("\n")
	while valid_num(pin)!=True:
		clear()
		print display[path] + "\nThat wasn't valid."
		pin = raw_input("")
	clear()
	xyz = "Your Name: " + name + "\nAccountID: " + uid + "\nYour PIN:  " + pin + "\nEnter y to confirm, enter n to restart.\n"
	print xyz
	confirm = raw_input("\n")
	while confirm not in ['y','n']:
		clear()
		print xyz
		confirm = raw_input("\n")
	insert_new_user(name,uid,pin)
	return confirm

def atm():
	path = '0'
	pathx(path)
	while 1:
		x = raw_input(">> atm$ ")
		if x == "0":
			clear()
			pathx(path)
		elif x == "1":
			login()
			clear()
			pathx(path)
		elif x == "2":
			while create_user()!='y':
				create_user()
			clear()
			pathx(path)
		elif x == "3":
			print "Thank you. Bye!\n"
			break
		else:
			print "No Such Option."

clear()
pathx('X')
pathx('Y')
atm()
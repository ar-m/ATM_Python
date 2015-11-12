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
	'7': "Verifying Login..."
}

last_fails = []
freeze_start = None

def is_frozen_and_should():
	global last_fails
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
	global freeze_start
	l = len(last_fails)
	if l>1 and last_fails[l-3]>time.time()-60:
		return True
	else:
		return False
#delete all of which are more than 60 seconds ago.

def freeze():
	global last_fails
	global freeze_start
	freeze_start = time.time()
	last_fails = []

def fail(now):
	global last_fails
	global freeze_start
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
	if len(f) != 0:
		return True
	else:
		return False

def user_exists(uid):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	cursor.execute("SELECT * FROM Users WHERE User_ID=%s AND User_PIN!=%s", (uid,"xxxx"))
	f = cursor.fetchall()
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

def valid_amount(amount):
	pass

#This is a custom function made to display what is needed. while 1 display
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

def login():
	global last_fails
	global freeze_start
	if is_frozen_and_should():
		remaining = 60 - (time.time() - freeze_start)
		x = "The screen is frozen because of too many failed login attempts. " + str(remaining) + " seconds remaining."
		wait(x)
	else :
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
		if verify_id(uid,pin):
			wait("Login Success! Enter.")
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
import MySQLdb
def insert_new_user(name, uid, pin):
	cnx = MySQLdb.connect(host="127.0.0.1",user="root",passwd="staging9753",db="ATM")
	cursor = cnx.cursor()
	add_user = "INSERT INTO Users (User_ID, User_PIN, Full_Name, Num_Of_Accounts) VALUES (%s, %s, %s, %s)"
	data_user = (uid, pin, name, 0)
	cursor.execute(add_user,data_user)
	cnx.commit()
	cursor.close()
	cnx.close()

insert_new_user("Amine Messaoui", "1234", "4321")
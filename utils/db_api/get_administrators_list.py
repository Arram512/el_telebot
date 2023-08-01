from .init_connector import mycursor

def get_admins_list():
	mycursor.execute("SELECT telegram_id FROM users WHERE is_admin = 1")

	myresult = mycursor.fetchall()

	for admins_tuple in myresult:
		return admins_tuple
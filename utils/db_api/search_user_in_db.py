from .init_connector import mycursor

def search_user_in_db(users_data):
	mycursor.execute(f"SELECT * FROM users WHERE telegram_id = {users_data}")
	result = mycursor.fetchall()
	return result
from db_api import models

await models.create_db()

res = await models.DBCommander.get_non_admin_users()
print(res)
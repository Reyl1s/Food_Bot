from database.db_initializer import Database

class Users_DB:
    database: Database = None

    def __init__(self):
        self.database = Database()

    def create_user(self, user_id: int, nickname: str, name: str, phone: str):
        if (self.database):
            self.database.cursor.execute('INSERT OR IGNORE INTO `Users` (`User_Id`, `Nickname`, `Name`, Phone) VALUES (?,?,?,?)', (user_id, nickname, name, phone))
            self.database.conn.commit()

    def get_users(self):
        if (self.database):
            users = self.database.cursor.execute('SELECT * FROM `Users` WHERE `Is_Deleted` = 0')
            return users.fetchall()

    def get_users_id(self):
        if (self.database):
            users_id = self.database.cursor.execute('SELECT `User_Id` FROM `Users` WHERE `Is_Deleted` = 0')
            return users_id.fetchall()

    def get_deleted_users_id(self):
        if (self.database):
            users_id = self.database.cursor.execute('SELECT `User_Id` FROM `Users` WHERE `Is_Deleted` = 1')
            return users_id.fetchall()
    
    def get_user_by_id(self, user_id: int):
        if (self.database):
            user = self.database.cursor.execute('SELECT * FROM `Users` WHERE `Is_Deleted` = 0 AND `User_Id` = ?', (user_id,))
            user_from_database = user.fetchall()

            if len(user_from_database):
                return user_from_database[0]
            else:
                return None

    def get_user_phone_by_id(self, user_id: int):
        if (self.database):
            user = self.database.cursor.execute('SELECT `Phone` FROM `Users` WHERE `Is_Deleted` = 0 AND `User_Id` = ?', (user_id,))
            user_from_database = user.fetchall()

            if len(user_from_database):
                return user_from_database[0][0]
            else:
                return None

    def check_user(self, user_id: int):
        users_id_from_database = self.get_users_id()

        if users_id_from_database != None and len(users_id_from_database) and user_id in users_id_from_database[0]:
            return True
        
        return False

    def check_user_is_deleted(self, user_id: int):
        users_id_from_database = self.get_deleted_users_id()

        if users_id_from_database != None and len(users_id_from_database) and user_id in users_id_from_database[0]:
            return True
        
        return False

    def delete_user(self, user_id: int):
        if (self.database):
            self.database.cursor.execute('UPDATE `Users` SET `Is_Deleted` = true WHERE `User_Id` = ?', (user_id,))
            self.database.conn.commit()

    def get_user_id_by_nickname(self, user_nickname: str):
        if (self.database):
            user_id = self.database.cursor.execute('SELECT `User_Id` FROM `Users` WHERE `Is_Deleted` = 0 AND `Nickname` = ?', (user_nickname,))
            user_id_from_database = user_id.fetchall()

            if len(user_id_from_database):
                return user_id_from_database[0][0]
            else:
                return None
    
    def apply_user_requisites(self, user_id: int, requisites: str):
        if (self.database):
            self.database.cursor.execute('UPDATE `Users` SET `Requisites` = ? WHERE `User_Id` = ?', (requisites, user_id))
            self.database.conn.commit()

    def apply_user_name(self, user_id: int, user_name: str):
        if (self.database):
            self.database.cursor.execute('UPDATE `Users` SET `Name` = ? WHERE `User_Id` = ?', (user_name, user_id))
            self.database.conn.commit()
    
    def close(self):
        if (self.database):
            self.database.close_conn()

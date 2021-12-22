import sqlite3
from sqlite3 import Error


class Database:
    location = None
    connection = None
    cursor = None

    def __init__(self, location):
        self.location = location
        self.__create_table()

    def __open_connection(self):
        """Creates the connection with the database if the database does not already exist."""
        try:
            self.connection = sqlite3.connect(self.location)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def __close_connection(self):
        """Closes all the connections."""
        self.cursor.close()
        self.connection.close()

    def __create_table(self):
        """Creates the table containing username1, username2 and common key associated."""
        self.__open_connection()
        sql_request = """CREATE TABLE IF NOT EXISTS common_keys(
                                username1 text NOT NULL,
                                username2 text NOT NULL,
                                common_key text PRIMARY KEY);"""
        try:
            self.cursor.execute(sql_request)
        except Error as e:
            print(e)
        self.connection.commit()
        self.__close_connection()

    def add_new_line(self, username1, username2, common_key):
        """We add a common key for a new pair of users. To do when username1 has a new contact."""
        if username2 == "" or username1 == "" or common_key == "":
            return False
        if self.common_key_in_database(common_key):
            return False
        else:
            self.__open_connection()
            sql_insert_client = """INSERT INTO common_keys
             VALUES('""" + username1 + """','""" + username2 + """','"""+common_key+"""');"""
            self.cursor.execute(sql_insert_client)
            self.connection.commit()
            self.__close_connection()
            return True

    def common_key_in_database(self, common_key):
        """We need to check if the common key already exists in the database."""
        self.__open_connection()
        sql_select = """SELECT * FROM common_keys WHERE common_key = '""" + common_key + """';"""
        self.cursor.execute(sql_select)
        data = self.cursor.fetchall()
        self.__close_connection()
        if len(data) == 0:
            return False
        else:
            return True

    def select_contact_list(self, username):
        """We want to return all the username2 that have a common key with username1."""
        list_to_return = list()
        self.__open_connection()
        sql_select = """
            SELECT username1, username2
            FROM common_keys
            WHERE username1 = '""" + username + """' OR username2 = '""" + username + """';"""
        self.cursor.execute(sql_select)
        data = self.cursor.fetchall()
        for row in data:
            if row[0] == username:
                list_to_return.append(row[1])
            else:
                list_to_return.append(row[0])
        return list_to_return

    def select_common_key(self, username1, username2):
        """We want to select the common key between username1 and username2. If it doesn't exist, the string
        to return will be empty."""
        self.__open_connection()
        sql_select = """
        SELECT common_key
         FROM common_keys 
         WHERE (username1 = '""" + username1 + """' AND username2 = '""" + username2 + """') 
         OR (username1 = '""" + username2 + """' AND username2 = '""" + username1 + """'); """
        self.cursor.execute(sql_select)
        data = self.cursor.fetchall()
        string_to_return = data[0][0]
        return string_to_return

import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from psycopg2 import OperationalError


class StorageFunctions:
    load_dotenv(find_dotenv(filename=".env-vars"))

    def __init__(self, table_name, db_name=os.getenv("name"), db_user=os.getenv("user"), db_password=os.getenv("password"), db_host=os.getenv("host"), db_port=os.getenv("port")):
        self.connection = self._createconnection(db_name, db_user, db_password, db_host, db_port)
        self.table = table_name

    @staticmethod
    def _createconnection(db_name, db_user, db_password, db_host, db_port):
        connection = None
        try:
            connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        except OperationalError as error:
            print("The error", error, "occurred")
        return connection

    def _executequery(self, query, data, fetching=False):
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data)
            if fetching:
                result = cursor.fetchall()
                return result
        except OperationalError as error:
            print("The error", error, "occurred")

    def append(self, list_of_values, data):
        data_records = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO " + self.table + f" " + list_of_values + f" VALUES ({data_records})"
        self._executequery(query, data, fetching=False)
        return query

    def list(self, item):
        query = f"SELECT " + item + f" FROM " + self.table
        data = self._executequery(query, data=None, fetching=True)
        data_list = []
        for data_item in data:
            data_list.append(data_item[0])
        return data_list

    def retrieve(self, column_list, data_list, negative=False):
        query_condition = self.formquerycondition(column_list, data_list, False, negative=negative)
        query = f"SELECT * FROM " + self.table + " WHERE " + query_condition
        data_list = self._executequery(query, data=None, fetching=True)
        return list(data_list)

    def update(self, column_list, data_list, identifier_value, identifier_name="id"):
        query_condition = self.formquerycondition(column_list, data_list, True)
        query = f"UPDATE " + self.table + " SET " + query_condition + " WHERE " + identifier_name + " = '" + str(identifier_value) + "'"
        self._executequery(query, data=None, fetching=False)

    @staticmethod
    def formquerycondition(column_list, data_list, updating=False, negative=False):
        assert len(column_list) == len(data_list), "Columns list and data list lengths do not match"
        query_condition = ""
        for counter in range(len(column_list)):
            if data_list[counter] is not None:
                query_condition = query_condition + column_list[counter] + " = '" + str(data_list[counter]) + "'"
            else:
                if updating:
                    query_condition = query_condition + column_list[counter] + " = null"
                else:
                    query_condition = query_condition + column_list[counter] + " is null"
            if updating:
                query_condition = query_condition + ", "
            else:
                query_condition = query_condition + " AND "
        if updating:
            query_condition = query_condition[:-2]
        else:
            query_condition = query_condition[:-5]
        if negative:
            query_condition = query_condition.replace("is", "is not")
            query_condition = query_condition.replace("=", "!=")
        return query_condition

    def delete(self, identifier_value, identifier_name="id"):
        query = f"DELETE FROM " + self.table + " WHERE " + identifier_name + " = '" + str(identifier_value) + "'"
        self._executequery(query, data=None, fetching=False)

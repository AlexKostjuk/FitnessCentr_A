import sqlite3
from flask import Flask, request, render_template, session, redirect
from functools import wraps


def dict_factory(cursor, row):
    d={}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Dbsql:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = dict_factory
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()


    def fetch_oll(self, table, colons = None, condition = None, join_table = None, join_condition = None):
        # join_condition =
        if colons is not None:
            print(colons, len(colons))
            if type(colons) == list:
                colons_str = ', '.join(colons)
                print(colons_str)
                qvery = f'select {colons_str} from {table}'
            else:
                qvery = f'select {colons} from {table}'

        else:
            qvery = f'select * from {table}'
        conditions = []

        if join_table is not None:
            if type(join_table) is not list:
                join_cond_list = []
                for key, val in join_condition.items():
                    join_cond_list.append(f"{key}={val}")
                join_cond_str = " and ".join(join_cond_list)
                join_str = f" join {join_table} ON {join_cond_str} "
                qvery = qvery + join_str
            else:
                join_cond_list = []
                for key, val in join_condition.items():
                    join_cond_list.append(f"{key}={val}")
                join_cond_str = " and ".join(join_cond_list)
                join_str_fin = ''
                for i in join_table:

                    join_str = f" join {str(i)} ON {str(i)}.{join_cond_str} "
                    join_str_fin += join_str
                qvery = qvery + join_str_fin



        if condition is not None:
            for key, val in condition.items():
                conditions.append(f"{key}='{val}' ")
            str_conditions = " and ".join(conditions)
            str_conditions = " where " + str_conditions
            qvery = qvery + str_conditions
        print(qvery)
        cursor = self.connection.cursor()
        cursor.execute(qvery)
        res = cursor.fetchall()
        if res:
            return res
        return None


    def fetch_one(self, table, colons = None, condition = None, join_table = None, join_condition = None):
        # join_condition =
        # qvery = f'select * from {table}'
        if colons is not None:
            print(colons, len(colons))
            if type(colons) == list:
                colons_str = ', '.join(colons)
                print(colons_str)
                qvery = f'select {colons_str} from {table}'
            else:
                qvery = f'select {colons} from {table}'

        else:
            qvery = f'select * from {table}'
        conditions = []

        if join_table is not None:
            if join_condition is not None:

                join_cond_list = []
                for key, val in join_condition.items():
                    join_cond_list.append(f"{key}={val}")
                join_cond_str = " and ".join(join_cond_list)
                join_str = f" join {join_table} ON {join_cond_str} "
            else:
                join_str = f' join {join_table} '
            qvery = qvery + join_str



        if condition is not None:
            for key, val in condition.items():
                conditions.append(f"{key}='{val}' ")
            str_conditions = " and ".join(conditions)
            str_conditions = " where " + str_conditions
            qvery = qvery + str_conditions
        cursor = self.connection.cursor()
        cursor.execute(qvery)
        res = cursor.fetchone()
        if res:
            return res
        return None

    # def fetch_one(self, qvery, *args, **kwargs):
    #     cursor = self.connection.cursor()
    #     cursor.execute(qvery, *args, **kwargs)
    #     res = cursor.fetchone()
    #     if res:
    #         return res
    #     return None

    def insert_to_db(self, table, data):
        keys = []
        vals = []
        for key, value in data.items():
            keys.append(key)
            vals.append("'"+str(value)+"'")
        str_keys = ', '.join(keys)
        str_vals = ', '.join(vals)
        qvery = f"INSERT INTO {table} ({str_keys}) VALUES ({str_vals})"

        cursor = self.connection.cursor()
        cursor.execute(qvery)
        self.connection.commit()

    def update_db(self, table, data, condition):
        keys = []
        vals = []
        for key, value in data.items():
            keys.append(key)
            vals.append("'" + str(value) + "'")
        str_keys_vals = ', '.join([f"{key} = {val}" for key, val in zip(keys, vals)])
        keys_c = []
        vals_c = []
        for key, value in condition.items():
            keys_c.append(key)
            vals_c.append("'" + str(value) + "'")
        str_keys_vals_c = ' AND '.join([f"{key} = {val}" for key, val in zip(keys_c, vals_c)])
        query = f"UPDATE {table} SET {str_keys_vals} WHERE {str_keys_vals_c}"

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def delete_from_db(self, table, condition):
        keys = []
        for key in condition.keys():
            keys.append(key + " = ?")
        str_keys = ' AND '.join(keys)
        qvery = f"DELETE FROM {table} WHERE {str_keys}"

        cursor = self.connection.cursor()
        cursor.execute(qvery, tuple(condition.values()))
        self.connection.commit()



def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        results = func(*args, **kwargs)
        return results
    return wrapper
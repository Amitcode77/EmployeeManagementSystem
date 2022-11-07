from flask import g
import sqlite3


def connect_to_database():
    sql = sqlite3.connect('C:/Users/ASUS/PycharmProjects/EMS/employeeapplication.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_database():
    if not hasattr(g, 'employeeapplication'):
        g.employeeapplication = connect_to_database()

    return g.employeeapplication

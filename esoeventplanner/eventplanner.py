import datetime
import sqlite3
from os import path
from sys import exit

class eventplanner (object):
    def __init__(self, servername):
        self.servername = servername
        self.daysofweek = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }
        self.monthsofyear = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        self._DBOPEN_()

    def __del__(self):
        self._DBCLOSE_()

    def initalize(self):
        ''' This will create the database for the events named, events.db. If it detects this file it will not be run again for protection'''
        print ("initalizing server {}".format(self.servername))
        self.cursor.execute("""CREATE TABLE events (
                           date text,
                           author text,
                           description text,
                           time text,
                           host text
                       )""")
        return ("The database and table has been created.")

    def _DBOPEN_(self):
        self.conn = sqlite3.connect("{}.db".format(self.servername))
        self.cursor = self.conn.cursor()

    def _DBCLOSE_(self):
        self.cursor.close()
        self.conn.close()

    def create_event(self, date, description, time, host, author):
        self.createquery = """INSERT INTO events(date, author, description, time, host)
                                VALUES (?, ?, ?, ?, ?)"""
        self.createvalues = (date, author, description, time, host)
        self.cursor.execute(self.createquery, self.createvalues)
        self.conn.commit()

    def get_all_events(self, specdate):
        return(self.cursor.execute("SELECT * FROM events WHERE date = '%s'" % specdate).fetchall())

    def get_event_by_date(self, date):
        self.getquery = """SELECT * FROM events where date=?"""
        self.queryvars = (date,)
        return self.cursor.execute(self.getquery, self.queryvars)

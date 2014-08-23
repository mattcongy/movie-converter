#!/usr/bin/python

import sqlite3
from mconverter import config
from os.path import join
class ConverterDB(object):
    """docstring for ConverterDB"""
    def __init__(self, dbpath = config.mc_db_path):
        super(ConverterDB, self).__init__()
        self.dbpath = dbpath


    def getConnection(self):
        con = sqlite3.connect(self.dbpath)
        return con


    def initDB(self):
        con = self.getConnection()
        con.execute("""CREATE TABLE Movies(
                                      ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                      Name TEXT,
                                      MD5SUM TEXT)""")
        con.close()

    def insertMovie(self,MovieFile):
        con = self.getConnection()
        cur = con.cursor()

        cur.execute("INSERT INTO Movies(Name,MD5SUM) VALUES (?,?)",(MovieFile.name,MovieFile.md5))
        con.commit()
        cur.close()
        con.close()

    def getMovieInfo(self,MD5Hash):
        con = self.getConnection()
        cur = con.cursor()
        cur.execute("""SELECT ID, Name FROM Movies WHERE MD5SUM = ?""",(MD5Hash,))
        row = cur.fetchone()
        cur.close()
        con.close()

        return row


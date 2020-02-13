"""
A heleper functions for using database with two functions.
1) Creating the connection 
2) Returning the database 
"""

#-- g is a place holder and global object that can holds anydata 
from flask import g 

#-- sqlite3 as a test database 
import sqlite3 


#-- creates a connection 
def connect_db():
	sql = sqlite3.connect("school.db") #-- database's file name 
	#-- it will be replaced by MySQL URI
	sql.row_factory = sqlite3.Row  

	return sql 

#-- getting the connection object 
def get_db():
	if not hasattr(g, "sqlite_db"):
		g.sqlite_db = connect_db()
	return g.sqlite_db 



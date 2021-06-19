from datetime import datetime as dt
import sqlite3

def make_conn():
	conn = sqlite3.connect('abridge.db', detect_types=sqlite3.PARSE_DECLTYPES)
	conn.row_factory = sqlite3.Row
	return conn

def get(nick):
	conn = make_conn()
	row = conn.execute('SELECT * FROM links WHERE nick = ?', (nick, ) ).fetchone()
	if row == None:
		return False
	conn.execute('UPDATE links SET clicks = ? WHERE nick = ?',
		(row['clicks'] + 1, nick) )
	conn.commit()
	conn.close()
	return row['address']

def insert(nick, address):
	conn = make_conn()
	delete(nick)
	conn.execute('INSERT INTO links VALUES (?,?,?,?)', 
		(nick, address, 0, dt.now()) )
	conn.commit()
	conn.close()

def delete(nick):
	conn = make_conn()
	conn.execute('DELETE FROM links WHERE nick = ?', 
		(nick, ) )
	conn.commit()
	conn.close()

def select_all():
	conn = make_conn()
	rows = conn.execute('SELECT * FROM links').fetchall()
	conn.close()
	return rows

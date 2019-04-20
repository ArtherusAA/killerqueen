rom django.shortcuts import render
import killer.DataBaseControl as db
import squilt3
# Create your views here.

conn = sqlite3.connect("killer.DataBaseControl.db")
cursor = conn.cursor()

def add_user(name):
    cursor.execute("""INSERT INTO players VALUES(name, kills, wins)""", (name, '0', '0'))
    cursor.commit()

def set_kills(name, kills):
    sql = "SELECT * FROM players WHERE player =?"
    result = cursor.execute(sql, [(name)]) 
    sql = """UPDATE players SET player = kills WHERE player = result.kills"""
    cursor.execute(sql)
    conn.commit()


def set_wins(name, wins):
    sql = "SELECT * FROM players WHERE player =?"
    result = cursor.execute(sql, [(name)]) 
    sql = """UPDATE players SET player = wins WHERE player = result.wins"""
    cursor.execute(sql)
    conn.commit()

"""
    db.add_user(name)
    db.set_kills(name, kills)
    db.set_wins(name, wins)
"""
conn.close()

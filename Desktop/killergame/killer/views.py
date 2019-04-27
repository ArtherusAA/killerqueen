from django.shortcuts import render
import killer.DataBaseControl as db
import squilt3 
# Create your views here.

conn = sqlite3.connect("scoreboard.sqlite3") # создаем соединение с базой данной
cursor = conn.cursor() # создаем курсор для работы


def add_user(name):
    cursor.execute("""INSERT INTO players VALUES(?, ?, ?)""", (name, '0', '0')) # add new playes to scroboard
    cursor.commit() # commit


def set_kills(name, kills):
    sql = "SELECT * FROM players WHERE player = ?" # find player in table
    result = cursor.execute(sql, [(name)]) # result from sql with name
    sql = ("""UPDATE players SET player = ? WHERE player = ?""", (kills, result.kills)) # set players kills 
    cursor.execute(sql) # ending
    conn.commit() # commit


def set_wins(name, wins):
    sql = "SELECT * FROM players WHERE player = ?" # find player in table
    result = cursor.execute(sql, [(name)]) # result from sql with name
    sql = ("""UPDATE players SET player = ? WHERE player = ?""", (wins, result.wins)) # set players wins
    cursor.execute(sql) # ending
    conn.commit() # commit

conn.close() # close cursor and connected because we had been ended to work with this f**king table

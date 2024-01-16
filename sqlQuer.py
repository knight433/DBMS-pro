import mysql.connector

con = mysql.connector.connect(host='localhost',password = 'root1',user='root',database='players_stats')

class Database:
    def addPlayer(self,name,matches,role,team):
        cursor = con.cursor()
        sqlQue = 'INSERT INTO PLAYERS VALUES(%s,%s,%s,%s);'

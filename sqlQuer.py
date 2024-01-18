import mysql.connector

class Database:

    def uniqueID(self):
        qur = 'SELECT MAX(ID) AS max_id FROM players;'
        try:
            cursor = self.conn.cursor()
            cursor.execute(qur)
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            unique_id = max_id + 1
        except Exception as e:
            print(f"Error getting unique ID: {e}")
        finally:
            cursor.close()

        return unique_id

    def Addbatting(self,player_id,inng,runs,balls,notout,best):
        pass

    def addPlayer(self, name, matches, role, team):
        try:
            cursor = self.conn.cursor()

            # Get a unique ID
            player_id = self.uniqueID()

            sqlQue = 'INSERT INTO PLAYERS (ID, Name, Matches, Role, Team) VALUES (%s, %s, %s, %s, %s);'
            values = (player_id, name, matches, role, team)

            cursor.execute(sqlQue, values)
            self.conn.commit()
            print("Player added successfully.")

        except Exception as e:
            print(f"Error adding player: {e}")
        finally:
            cursor.close()
        
        return player_id


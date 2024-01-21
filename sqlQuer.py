import mysql.connector

class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost',password = 'root1',user='root',database='player_stats')

    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()


    def uniqueID(self):
        qur = 'SELECT MAX(ID) AS max_id FROM players;'
        try:
            cursor = self.conn.cursor()
            cursor.execute(qur)
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            unique_id = max_id + 1
        except Exception as e:
            unique_id = 1 
        finally:
            cursor.close()

        return unique_id

    def calculate_elo(self,strike_rate, runs, batting_avg, num_outs):
    
        weight_strike_rate = 0.2
        weight_runs = 0.3
        weight_avg = 0.3
        weight_num_outs = -0.2

        # Normalize values (you might want to adjust these scaling factors)
        normalized_strike_rate = strike_rate / 100
        normalized_runs = runs / 1000
        normalized_batting_avg = batting_avg / 100
        normalized_num_outs = num_outs / 50

        # Calculate the weighted sum
        weighted_sum = (
            weight_strike_rate * normalized_strike_rate +
            weight_runs * normalized_runs +
            weight_avg * normalized_batting_avg +
            weight_num_outs * normalized_num_outs
        )

        # Adjust the range of the result to represent an Elo-like scale
        elo_scale = 1000
        player_elo = (weighted_sum - 0.5) * elo_scale

        return player_elo


    def AddBattingInfo(self,player_id,battingHistory):
        l = ['Rspin','Lspin','Rpace','Lpace']
        runs_to_Lspin = battingHistory['runs_to_Lspin']
        runs_to_Rspin = battingHistory['runs_to_Rspin']
        runs_to_Rpace = battingHistory['runs_to_Rpace']
        runs_to_Lpace = battingHistory['runs_to_Lpace']
        out_to_Lspin = battingHistory['out_to_Lspin']
        out_to_Rspin = battingHistory['out_to_Rspin']
        out_to_Rpace = battingHistory['out_to_Rpace']
        out_to_Lpace = battingHistory['out_to_Lpace']
        balls_Lspin = battingHistory['balls_Lspin']
        balls_Rspin = battingHistory['balls_Rspin']
        balls_Rpace = battingHistory['balls_Rpace']
        balls_Lpace = battingHistory['balls_Lpace']
        avg_Rspin = runs_to_Rspin / out_to_Rspin if out_to_Rspin != 0 else 0
        avg_Lspin = runs_to_Lspin / out_to_Lspin if out_to_Lspin != 0 else 0
        avg_Rpace = runs_to_Rpace / out_to_Rpace if out_to_Rpace != 0 else 0
        avg_Lpace = runs_to_Lpace / out_to_Lpace if out_to_Lpace != 0 else 0
        strike_rate_Lspin = (runs_to_Lspin / balls_Lspin) * 100 if balls_Lspin != 0 else 0
        strike_rate_Rspin = (runs_to_Rspin / balls_Rspin) * 100 if balls_Rspin != 0 else 0
        strike_rate_Rpace = (runs_to_Rpace / balls_Rpace) * 100 if balls_Rpace != 0 else 0
        strike_rate_Lpace = (runs_to_Lpace / balls_Lpace) * 100 if balls_Lpace != 0 else 0
        
        eloRspin = self.calculate_elo(strike_rate_Rspin, runs_to_Rspin, avg_Rspin, out_to_Rspin)
        eloLspin = self.calculate_elo(strike_rate_Lspin, runs_to_Lspin, avg_Lspin, out_to_Lspin)
        eloRpace = self.calculate_elo(strike_rate_Rpace, runs_to_Rpace, avg_Rpace, out_to_Rpace)
        eloLpace = self.calculate_elo(strike_rate_Lpace, runs_to_Lpace, avg_Lpace, out_to_Lpace)
        eloList = [eloRspin,eloLspin,eloRpace,eloLpace]

        prefBowler = l[eloList.index(max(eloList))]
        prefpos = battingHistory['pos']
        
        ing = battingHistory['inng']
        runs = runs_to_Lspin + runs_to_Rspin + runs_to_Rpace + runs_to_Lpace
        balls = balls_Lspin + balls_Rspin + balls_Rpace + balls_Lpace
        out = out_to_Lspin + out_to_Rspin + out_to_Lpace + out_to_Rpace
        best = battingHistory['best']
        sr = (runs/balls) * 100
        avg = runs/out if out != 0 else 0

        sqlQurHistoy = 'INSERT INTO battinghistory VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        sqlQurstats = 'INSERT INTO battingstats VALUES (%s, %s, %s, %s, %s, %s)'
        sqlQurbio = 'INSERT INTO battingbio (%s, %s, %s,)'

        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlQurHistoy, (player_id,runs_to_Lspin,runs_to_Rspin,runs_to_Rpace ,runs_to_Lpace ,out_to_Lspin ,out_to_Rspin,out_to_Rpace,out_to_Lpace ,balls_Lspin,balls_Rspin,balls_Rpace,balls_Lpace,avg_Lspin, avg_Rspin, avg_Rpace, avg_Lpace,eloRspin,eloLspin,eloRpace,eloLpace))
            cursor.execute(sqlQurstats,(player_id,ing,runs,sr,avg,best))
            cursor.execute(sqlQurbio,(player_id,prefBowler,prefpos))
            self.conn.commit()
            print("Player added successfully.")
        except Exception as e:
            print(f"Error adding player: {e}")
        finally:
            cursor.close()
   
    def addPlayer(self,name,matches,role,team,bowlingType,battingType):
        
        sqlQur = 'INSERT INTO PLAYER VALUES (%s, %s, %s, %s, %s, %s, %s)'
        id = self.uniqueID()

        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlQur, (id,name, matches, role, team, bowlingType, battingType))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding player: {e}")
        finally:
            cursor.close()

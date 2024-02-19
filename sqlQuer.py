import mysql.connector

class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost',password = 'root1',user='root',database='player_stats')

    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()


    def uniqueID(self):
        qur = 'SELECT MAX(player_id) AS max_id FROM player;'
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

    def calculate_elo_batting(self,strike_rate, runs, batting_avg, num_outs):
    
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
        elo_scale = 100
        player_elo = (weighted_sum - 0.5) * elo_scale

        return round(player_elo,2)
    
    def calculate_bowling_elo(self, strike_rate, wickets):
        
        elo = strike_rate/10
        return elo

    def AddBowlingInfo(self,player_id,bowlingHistory):
        l = ['left','right']
        runs_to_right = bowlingHistory['runs_to_right']
        runs_to_left = bowlingHistory['runs_to_left']
        wickets_to_right = bowlingHistory['wickets_to_right']
        wickets_to_left = bowlingHistory['wickets_to_left']
        balls_to_right = bowlingHistory['balls_to_right']
        balls_to_left = bowlingHistory['balls_to_left']
        inng = bowlingHistory['inngs']
        best = bowlingHistory['best']
        pos = bowlingHistory['pos']

        Totalruns = runs_to_left + runs_to_right
        totalballs = balls_to_left + balls_to_right
        totalWickets = wickets_to_left + wickets_to_right
        eco = round(totalballs/(totalballs),2) if totalballs != 0 else 0

        avg_right = round(runs_to_right / wickets_to_right, 2) if wickets_to_right != 0 else 0
        avg_left = round(runs_to_left / wickets_to_left, 2) if wickets_to_left != 0 else 0
        strike_rate_right = round(balls_to_right / wickets_to_right ,2)  if balls_to_right and wickets_to_right != 0 else 0
        strike_rate_left = round(balls_to_left / wickets_to_left ,2)  if balls_to_left and wickets_to_left != 0 else 0

        elo_right = self.calculate_bowling_elo(strike_rate_right,wickets_to_right)
        elo_left = self.calculate_bowling_elo(strike_rate_left,wickets_to_left)
        eloList = [elo_left,elo_right]
        prefbat = l[eloList.index(max(eloList))]

        sqlHistory = 'INSERT INTO bowlinghistory VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );'
        sqlStats = 'INSERT INTO bowlingstats VALUES(%s, %s, %s, %s, %s, %s);'
        sqlbio = 'INSERT INTO bowlingbio VALUES(%s, %s, %s);'

        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlHistory,(player_id,runs_to_left,runs_to_right,wickets_to_left,wickets_to_right,balls_to_left,balls_to_right,avg_left,avg_right,elo_left,elo_right,strike_rate_right,strike_rate_left))
            cursor.execute(sqlStats,(player_id,inng,totalWickets,Totalruns,eco,best))
            cursor.execute(sqlbio,(player_id,prefbat,pos))
            self.conn.commit()
            print(f'added bowling stats of {player_id}') #debugging
        except Exception as e:
            print(f"Error adding player: {e}")
        finally:
            cursor.close()


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
        
        avg_Rspin = round(runs_to_Rspin / out_to_Rspin, 2) if out_to_Rspin != 0 else 0
        avg_Lspin = round(runs_to_Lspin / out_to_Lspin, 2) if out_to_Lspin != 0 else 0
        avg_Rpace = round(runs_to_Rpace / out_to_Rpace, 2) if out_to_Rpace != 0 else 0
        avg_Lpace = round(runs_to_Lpace / out_to_Lpace, 2) if out_to_Lpace != 0 else 0

        strike_rate_Lspin = (runs_to_Lspin / balls_Lspin) * 100 if balls_Lspin != 0 else 0
        strike_rate_Rspin = (runs_to_Rspin / balls_Rspin) * 100 if balls_Rspin != 0 else 0
        strike_rate_Rpace = (runs_to_Rpace / balls_Rpace) * 100 if balls_Rpace != 0 else 0
        strike_rate_Lpace = (runs_to_Lpace / balls_Lpace) * 100 if balls_Lpace != 0 else 0
        
        eloRspin = self.calculate_elo_batting(strike_rate_Rspin, runs_to_Rspin, avg_Rspin, out_to_Rspin)
        eloLspin = self.calculate_elo_batting(strike_rate_Lspin, runs_to_Lspin, avg_Lspin, out_to_Lspin)
        eloRpace = self.calculate_elo_batting(strike_rate_Rpace, runs_to_Rpace, avg_Rpace, out_to_Rpace)
        eloLpace = self.calculate_elo_batting(strike_rate_Lpace, runs_to_Lpace, avg_Lpace, out_to_Lpace)
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
        sqlQurHistoy = 'INSERT INTO battinghistory VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        sqlQurstats = 'INSERT INTO battingstats VALUES (%s, %s, %s, %s, %s, %s);'
        sqlQurbio = 'INSERT INTO battingbio VALUES (%s, %s, %s);'

        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlQurHistoy, (player_id,runs_to_Lspin,runs_to_Rspin,runs_to_Rpace ,runs_to_Lpace ,out_to_Lspin ,out_to_Rspin,out_to_Rpace,out_to_Lpace ,balls_Lspin,balls_Rspin,balls_Rpace,balls_Lpace,avg_Lspin, avg_Rspin, avg_Rpace, avg_Lpace,eloLspin,eloRspin,eloRpace,eloLpace))
            cursor.execute(sqlQurstats,(player_id,ing,runs,sr,avg,best))
            cursor.execute(sqlQurbio,(player_id,prefBowler,prefpos))
            self.conn.commit()
            print(f'added batting info of {player_id}') #debugging
        except Exception as e:
            print(f"Error adding player: {e}")
        finally:
            cursor.close()
   
    def addPlayer(self,name,matches,role,team,bowlingType,battingType,batdic,bowldic):
        
        sqlQur = 'INSERT INTO PLAYER VALUES (%s, %s, %s, %s, %s, %s, %s)'
        id = self.uniqueID()

        try:
            cursor = self.conn.cursor()
            cursor.execute(sqlQur, (id, name, matches, role, bowlingType, battingType, team))
            self.conn.commit()
            print('added player') #debugging
        except Exception as e:
            print(f"Error adding player: {e}")
        finally:
            cursor.close()

        self.AddBattingInfo(id,batdic)
        self.AddBowlingInfo(id,bowldic)

    def executeQur(self,qur):
        cursor = self.conn.cursor()
        cursor.execute(qur)
            
        rt = cursor.fetchall()
        return rt
        

    def getBattingInfo(self,player_id,req):
        
        qur = f'SELECT * FROM battingbio WHERE player_id = {player_id};'
        batBio = self.executeQur(qur)
        batBio = batBio[0]

        if req == 'prefered_bowler':
            return batBio[1]
        elif req == 'prefered_postion':
            return batBio[2]
        else:
            print('not a valid req')
        
    def getbowlinInfo(self, player_id,req):
        
        qur = f'SELECT * FROM bowlingbio WHERE player_id ={player_id};'
        bowlbio = self.executeQur(qur)
        bowlbio = bowlbio[0]

        if req == 'prefered_batting_hand':
            return bowlbio[1]
        elif req == 'prefered_pos':
            return bowlbio[2]
        else:
            print('not a Valid request') 

    def playerInfo(self,player_id,req):
        
        qur = f'SELECT * FROM player WHERE player_id = {player_id}'
        playerInfo = self.executeQur(qur)
        playerInfo = playerInfo[0]

        if req == 'batting_hand':
            return playerInfo[6]
        elif req == 'bowlingType':
            return playerInfo[5]
        elif req == 'team':
            return playerInfo[4]
        elif req == 'role':
            return playerInfo[3]
        elif req == 'name':
            return playerInfo[1]
        

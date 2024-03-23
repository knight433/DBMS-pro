# app.py
from flask import Flask, render_template, request, jsonify,url_for,redirect
import backend 

app = Flask(__name__)
con = backend.database()

def testFuntion(player_info,batting_dic,bowling_dic):
    
    for key in batting_dic.keys():
        print(key,type(batting_dic[key]))

def customFuntion(l):
    retList = eval(l)
    return retList
    

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/addPlayer')
def addPlayersPage():
    return render_template('addPlayer.html')

@app.route('/comparePlayer')
def compareTeamPage():
    return render_template('compareTeams.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        
        data = request.json

        player_info = data.get('playerInfo', {})
        batting_dic = data.get('battingDic', {})
        bowling_dic = data.get('bowlingDic', {})

        # testFuntion(player_info,batting_dic,bowling_dic)

        con.addPlayer(player_info,batting_dic,bowling_dic)
        

        return jsonify({'message': 'Data received successfully'}), 200

@app.route('/compareTeam', methods=['POST'])
def compare_team():
    if request.method == 'POST':
        global team1_info
        global team2_info
        
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')

        team1_info, team2_info = con.GetTeam(team1, team2)
        para = [team1_info,team2_info]
        return render_template('compareWithPlayers.html',team=para)

@app.route('/getTeam', methods=['POST'])
def getTeam():
    global team1_info
    global team2_info

    allteam1 = list(team1_info.keys())  
    allteam2 = list(team2_info.keys())

    selteam1 = []
    selteam2 = []
    
    if request.method == 'POST':
        selected_players = request.form['cmpTeam']
        selected_players = customFuntion(selected_players)       

        for player in selected_players:
            
            if int(player) in allteam1:
                selteam1.append(player)
            elif int(player) in allteam2:
                selteam2.append(player)

        team1Bal = con.judgeTeam(selteam1)
        team2Bal = con.judgeTeam(selteam2)

        team1Players = []
        team2Players = []

        for i in selteam1:
            tempName = con.getName(i)
            team1Players.append(tempName)
        
        for i in selteam2:
            tempName = con.getName(i)
            team2Players.append(tempName)

        compScore = con.compareTeamStrength(selteam1,selteam2)

        para = [team1Bal,team2Bal,compScore,team1Players,team2Players]

        return render_template('Score.html',paras = para)
    
@app.route('/handle_player_click', methods=['GET','POST'])
def handle_player_click():
   if request.method == 'POST':
        player_name = request.form['player']
        print("Player clicked:", player_name)
        paraList = con.getPlayerStats(player_name)
        print(paraList)
        return render_template('playerPageSom.html',paras=paraList)

if __name__ == '__main__':
    app.run(debug=True)

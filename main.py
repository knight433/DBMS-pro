# app.py
from flask import Flask, render_template, request, jsonify,url_for,redirect
from sympy import per
import backend 

app = Flask(__name__)
con = backend.database()

def testFuntion(player_info,batting_dic,bowling_dic):
    
    for key in batting_dic.keys():
        print(key,type(batting_dic[key]))

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
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')

        team1_info, team2_info = con.compareTeam(team1, team2)
        para = [team1_info,team2_info]
        return render_template('compareWithPlayers.html',team=para)

@app.route('/getTeam', methods=['POST'])
def getTeam():
    if request.method == 'POST':
        print(request.form['cmpTeam'])
        return "Done"


if __name__ == '__main__':
    app.run(debug=True)

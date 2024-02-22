import sqlQuer

class database:
    def __init__(self):
        self.db = sqlQuer.Database() 
    
    def addPlayer(self,playerInfo,battingdic,bowlingdic):

        name = playerInfo['name']
        matches = playerInfo['played']
        role = playerInfo['role']
        team = playerInfo['team']
        bowlingType = playerInfo['bowlingType']
        battingType = playerInfo['battingHand']

        self.db.addPlayer(name,matches,role,team,bowlingType,battingType,battingdic,bowlingdic)
    
    def compareTeam(self,team1,team2):
        
        team1ID = self.db.getAllFromTeam(team1)
        team2ID = self.db.getAllFromTeam(team2)
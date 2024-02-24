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
    
    def compareTeam(self, team1, team2):
        team1ID = self.db.getAllFromTeam(team1)
        team2ID = self.db.getAllFromTeam(team2)

        team1info = {}
        team2info = {}

        for i in team1ID:
            tempName = self.db.playerInfo(i, 'name')
            tempRole = self.db.playerInfo(i, 'role')
            tempBatting = self.db.playerInfo(i, 'batting_hand')
            tempBowling = self.db.playerInfo(i, 'bowlingType')
            tempList = [tempName, tempRole, tempBatting, tempBowling]

            team1info[i] = tempList

        for i in team2ID:
            tempName = self.db.playerInfo(i, 'name')
            tempRole = self.db.playerInfo(i, 'role')
            tempBatting = self.db.playerInfo(i, 'batting_hand')
            tempBowling = self.db.playerInfo(i, 'bowlingType')
            tempList = [tempName, tempRole, tempBatting, tempBowling]

            team2info[i] = tempList

        return team1info, team2info

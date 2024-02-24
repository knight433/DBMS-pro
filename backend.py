import sqlQuer

class database:
    def __init__(self):
        self.db = sqlQuer.Database()
        self.goodThings = []
        self.badThings = []
    
    def addPlayer(self,playerInfo,battingdic,bowlingdic):

        name = playerInfo['name']
        matches = playerInfo['played']
        role = playerInfo['role']
        team = playerInfo['team']
        bowlingType = playerInfo['bowlingType']
        battingType = playerInfo['battingHand']

        self.db.addPlayer(name,matches,role,team,bowlingType,battingType,battingdic,bowlingdic)
    
    def GetTeam(self, team1, team2):
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

    def batsmenStrengthCount(self,batter_id,team):

        batterStrength = self.db.getBattingInfo(batter_id,'prefered_bowler')
        strCount = 0

        for player in team:

            role = self.db.playerInfo(player,'role')

            if role == "bowler" or role == "all-rounder":
                Btype = self.db.getbowlinInfo(player,)  
                
                if batterStrength == Btype:
                    strCount.append(player) 

            return strCount 
    
    #finds how many batsmen this bowler can dominate
    def bowlerStrengthCount(self,bowler_id,team):
    
        bowlerStrength = self.db.getbowlinInfo(bowler_id,'prefered_bowler')
        strCount = 0
        
        for player in team:
            role = self.db.playerInfo(player,'role')

            if role == 'batsmen' or role == 'all-rounder':
                hand = self.db.playerInfo(player,'batting_hand')
                
                if hand == bowlerStrength:
                    strCount.append(player)

    #scores out of 30 to judge a batting line up
    def judgeBatting(self,batsmen):
        
        rectop = 3
        recmiddle = 3
        lower = 1

        topScore = 0
        middleScore = 0
        lowerScore = 0
        
        for i in batsmen:
            pos = self.db.getBattingInfo(i,'prefered_postion')
            name = self.db.playerInfo(i,'name')
            if pos == 'top':
                rectop -= 1
            elif pos == 'middle':
                recmiddle -= 1
            elif pos == 'lower':
                lower -= 1
        
        if rectop <= 0:
            topScore = 10
            self.goodThings.append('There are enough top order batsmen') #report 
        else:
            topScore += 10 - (2*rectop)
            print(f'There are not enough top order batsmen hence top score = {topScore}') #report
        
        if recmiddle <= 10:
            middleScore += 10
            self.goodThings.append('There are enough middle order batsmen') #report
        else:
            middleScore += 10 - (2*recmiddle) + (-1*rectop)
            self.badThings.append(f'There are not enough middle order batsmen hence middle score = {middleScore}') #report

        if lower <= 0:
            lowerScore += 10
            self.goodThings.append('There are enough lower order batsmen') #report
        else:
            lowerScore += 10 - (2*lowerScore) + (-1*recmiddle)
            self.badThings.append(f'There are not enough lower order batsmen hence lower score = {lowerScore}') #report

        finalScore = topScore + middleScore + lowerScore
        return finalScore
    
    #scores out of 30 to judge a bowling  line up
    def judgebowling(self,bowlers):
        
        recOpen = 2
        recChange = 3
        recDeath = 1

        secondChange = 0
        openscore = 0
        changescore = 0
        deathscore = 0


        for bowler in bowlers:
            pos = self.db.getbowlinInfo(bowler,'prefered_pos')

            if pos == 'new':
                recOpen -= 1
            elif pos == 'first_change':
                recChange -= 1
            elif pos == 'second_change':
                recChange -= 1
                secondChange += 1
            elif pos == 'death':
                print('here',pos) #debugging
                recDeath -= 1
        
        if recOpen <= 0:
            openscore += 10
            self.goodThings.append('There are enough open bowlers') #report
        else:
            openscore += 10 - (3*recOpen)
            self.badThings.append('There are not enough new bowlers') #report
        
        if recChange <= 0:
            changescore += 10
            self.goodThings.append('There are enough change bowlers') #report
        else:
            changescore += 10 - (2*recChange) + (1*recOpen)        
            self.badThings.append('there are not enough change bowlers') #report
        
        if recDeath <= 0:
            deathscore += 10
            self.goodThings.append('There are enough death bowlers') #report
        elif recChange < 0:
            deathscore += 5
            self.badThings.append('there are not enough death bowlers can manage') #report
        else:
            self.badThings.append('not enough death bowlers and not enough change')
        
        finalScore = openscore + changescore + deathscore
        return finalScore

    def judgeTeam(self,team):

        bat = []
        bowl = []
        keep = []

        minBowl = 5
        minBat = 5
        minKeep = 1

        recBowl = 6
        recBat = 7

        for player in team:
            
            role = self.db.playerInfo(player,'role')

            if role == 'batsman': 
                bat.append(player) 
            
            elif role == "bowler":
                bowl.append(player) 
            
            elif role == 'all-rounder':
                bowl.append(player) 
                bat.append(player) 
            
            elif role == 'wicketkeeper':
                bat.append(player) 
                keep.append(player) 
        
        batscore = 0  #/30 + 10
        bowlscore = 0 #/30 + 10 
        keepscore = 0 #/10

        if len(bat) > minBat:
            batscore += 10
            self.goodThings.append('There are enough batsmen') #report
        else:
            batscore += 10 - abs(len(bat) - recBat)
            self.badThings.append("There are not enough Batsmen") #report
        
        batscore += self.judgeBatting(bat)
        
        if len(bowl) > minBowl:
            bowlscore += 10
            self.goodThings.append('There are enough bowlers') #report
        else:
            bowlscore += 10 - abs(len(bowl) - recBowl)
            self.badThings.append("There are not enough bowlers") #report
        
        bowlscore += self.judgebowling(bowl)
        
        if len(keep) < minKeep:
            keepscore += 0
        else:
            keepscore += 10

        # print(f' bat = {batscore}, bowl = {bowlscore}, keep = {keepscore}') #debugging
        percentage = ((batscore + keepscore + bowlscore)/90) * 100
        percentage = round(percentage, 2)

        return percentage

    def battingStrength(self,batsman,bowlers):

        batsmanStrenth = self.db.getBattingInfo(batsman,'prefered_bowler')
        strcount = 0
        # print(batsmanStrenth) #debugging
        for bowler in bowlers:
            bowltype = self.db.playerInfo(bowler,'bowlingType')
            # print(f'type: {bowltype}') #debugging

            if bowltype == batsmanStrenth:
                strcount += 1

        # print(f'batsmen - {batsman} strCount - {strcount}') #debugging
        if strcount >= len(bowlers)/2:
            return 1
        else:
            return 0

    def bowlingStrength(self,bowler,batsmen):

        bowlerStength = self.db.getbowlinInfo(bowler,'prefered_batting_hand')
        strcount = 0

        for batsman in batsmen:
            batingtype = self.db.playerInfo(batsman,'batting_hand')

            if batingtype == bowlerStength:
                strcount += 1
        
        if strcount >= len(batsmen)/2:
            return 1
        else:
            return 0

    def compareTeamStrength(self,team1,team2):
    
        bat1 = []
        bowl1 = []
        keep1 = []

        team1Battingstr = 0
        team1Bowlingstr = 0
        team2Battingstr = 0
        team2Bowlingstr = 0

        for player in team1:
            
            role = self.db.playerInfo(player,'role')

            if role == 'batsman': 
                bat1.append(player) 
            
            elif role == "bowler":
                bowl1.append(player) 
            
            elif role == 'all-rounder':
                bowl1.append(player) 
                bat1.append(player) 
            
            elif role == 'wicketkeeper':
                bat1.append(player) 
                keep1.append(player) 

        bat2 = []
        bowl2 = []
        keep2 = []
        for player in team2:
            
            role = self.db.playerInfo(player,'role')

            if role == 'batsman': 
                bat2.append(player) 
            
            elif role == "bowler":
                bowl2.append(player) 
            
            elif role == 'all-rounder':
                bowl2.append(player) 
                bat2.append(player) 
            
            elif role == 'wicketkeeper':
                bat2.append(player) 
                keep2.append(player)

        for batter in bat1:
            team1Battingstr += self.battingStrength(batter,bowl2)
        
        for batter in bat2:
            team2Battingstr += self.battingStrength(batter,bowl1)
        
        for bowler in bowl1:
            team1Bowlingstr += self.bowlingStrength(bowler,bowl2)
        
        for bowler in bowl2:
            team2Bowlingstr += self.bowlingStrength(bowler,bowl1)

        finalScore = team1Bowlingstr - team2Bowlingstr
        
        return finalScore
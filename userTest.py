import sqlQuer

db = sqlQuer.Database()


battingdic = {
    'runs_to_Lspin' : 8,
    'runs_to_Rspin' : 9,
    'runs_to_Rpace' : 42,
    'runs_to_Lpace' : 15,
    'out_to_Lspin'  : 2,
    'out_to_Rspin'  : 4,
    'out_to_Rpace'  : 4,
    'out_to_Lpace'  : 1,
    'balls_Lspin'   : 10,
    'balls_Rspin'   : 10,
    'balls_Rpace'   : 44,
    'balls_Lpace'   : 15,
    'pos' : 'tail',
    'inng' : 33,
    'best' : 21
}

bowlingdic = {
    'runs_to_right'   : 2324,
    'runs_to_left'    : 1098,
    'wickets_to_right': 90,
    'wickets_to_left' : 37,
    'balls_to_right'  : 1607,
    'balls_to_left'   : 825,
    'inngs'           : 205,
    'best'            : '4/11',
    'pos'             : 'new'}

# db.addPlayer('M Shami',205,'bowler','GT','Rpace','right',battingdic,bowlingdic)

#finds how many bowlers this batsmen can dominate
def batsmenStrengthCount(batter_id,team):

    batterStrength = db.getBattingInfo(batter_id,'prefered_bowler')
    strCount = 0

    for player in team:

        role = db.playerInfo(player,'role')

        if role == "bowler" or role == "all-rounder":
            Btype = db.getbowlinInfo(player,)  
            
            if batterStrength == Btype:
                strCount.append(player) 

        return strCount 

#finds how many batsmen this bowler can dominate
def bowlerStrengthCount(bowler_id,team):
    
    bowlerStrength = db.getbowlinInfo(bowler_id,'prefered_bowler')
    strCount = 0
    
    for player in team:
        role = db.playerInfo(player,'role')

        if role == 'batsmen' or role == 'all-rounder':
            hand = db.playerInfo(player,'batting_hand')
            
            if hand == bowlerStrength:
                strCount.append(player) 
    
    return strCount

#scores out of 30 to judge a batting line up
def judgeBatting(batsmen):
    
    rectop = 3
    recmiddle = 3
    lower = 1

    topScore = 0
    middleScore = 0
    lowerScore = 0
    
    for i in batsmen:
        pos = db.getBattingInfo(i,'prefered_postion')

        if pos == 'top':
            rectop -= 1
        elif pos == 'middle':
            recmiddle -= 1
        elif pos == 'lower':
            lower -= 1
    
    if rectop <= 0:
        topScore = 10
    else:
        topScore += 10 - (2*rectop)
    
    if recmiddle <= 10:
        middleScore += 10
    else:
        middleScore += 10 - (2*recmiddle) + (-1*rectop)

    if lower <= 0:
        lowerScore += 10
    else:
        lowerScore += 10 - (2*lowerScore) + (-1*recmiddle)

    finalScore = topScore + middleScore + lowerScore
    return finalScore

#scores out of 30 to judge a bowling  line up
def judgebowling(bowlers):
    
    recOpen = 2
    recChange = 3
    recDeath = 1

    secondChange = 0
    openscore = 0
    changescore = 0
    deathscore = 0

    for bowler in bowlers:
        pos = db.getbowlinInfo(bowler,'prefered_pos')

        if pos == 'new':
            recOpen -= 1
        elif pos == 'first-change':
            recChange -= 1
        elif pos == 'second-change':
            recChange -= 1
            secondChange += 1
        elif pos == 'death':
            recDeath -= 1
    
    if recOpen <= 0:
        openscore += 10
    else:
        openscore += 10 - (3*recOpen)

    if recChange <= 0:
        changescore += 10
    else:
        changescore += 10 - (2*recChange) + (-1*recOpen)        

    if recDeath <= 0:
        deathscore += 1
    elif recChange > 0:
        deathscore += 5
  
    finalScore = openscore + changescore + deathscore
    return finalScore

def judgeTeam(team):

    bat = []
    bowl = []
    keep = []

    minBowl = 5
    minBat = 5
    minKeep = 1

    recBowl = 6
    recBat = 7

    for player in team:
        
        role = db.playerInfo(player,'role')

        if role == 'batsmen': 
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
    keepscore = 0 

    if len(bat) < minBat:
        batscore += len(bat)
    else:
        batscore += 10 - abs(len(bat) - recBat)
    
    batscore += judgeBatting(bat)
    
    if len(bowl) < minBowl:
        bowlscore += len(bowl)
    else:
        bowlscore += 10 - abs(len(bowl) - recBowl)
    
    bowlscore += judgebowling(bowl)
    
    if len(keep) < minKeep:
        keepscore += 0
    else:
        keepscore += 10

    print(f' bat = {batscore}, bowl = {bowlscore}, keep = {keepscore}') #debugging

def battingStrength(batsman,bowlers):

    batsmanStrenth = db.getBattingInfo(batsman,'prefered_bowler')
    strcount = 0

    for bowler in bowlers:
        bowltype = db.playerInfo(bowler,'bowlingType')

        if bowltype == batsmanStrenth:
            strcount += 1

    if strcount >= len(bowlers)/2:
        return 1
    else:
        return 0

def bowlingStrength(bowler,batsmen):

    bowlerStength = db.getbowlinInfo(bowler,'prefered_batting_hand')
    strcount = 0

    for batsman in batsmen:
        batingtype = db.playerInfo(batsman,'batting_hand')

        if batingtype == bowlerStength:
            strcount += 1
    
    if strcount >= len(batsmen)/2:
        return 1
    else:
        return 0

def compareTeamStrength(team1,team2):
    
    bat1 = []
    bowl1 = []
    keep1 = []

    team1str = 0
    team2str = 0

    for player in team1:
        
        role = db.playerInfo(player,'role')

        if role == 'batsmen': 
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
        
        role = db.playerInfo(player,'role')

        if role == 'batsmen': 
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
        team1str += battingStrength(batter,bowl2)
    
    for batter in bat2:
        team2str += battingStrength(batter,bowl1)
    
    finalScore = team1str - team2str
    
    return finalScore


def testFuntion():
    team1 = [i for i in range(1,12)]
    judgeTeam(team1)

testFuntion()
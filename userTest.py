import sqlQuer

db = sqlQuer.Database()

goodThings = []
badThings = []

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
        name = db.playerInfo(i,'name')
        if pos == 'top':
            rectop -= 1
        elif pos == 'middle':
            recmiddle -= 1
        elif pos == 'lower':
            lower -= 1
    
    if rectop <= 0:
        topScore = 10
        goodThings.append('There are enough top order batsmen') #report 
    else:
        topScore += 10 - (2*rectop)
        print(f'There are not enough top order batsmen hence top score = {topScore}') #report
    
    if recmiddle <= 10:
        middleScore += 10
        goodThings.append('There are enough middle order batsmen') #report
    else:
        middleScore += 10 - (2*recmiddle) + (-1*rectop)
        badThings.append(f'There are not enough middle order batsmen hence middle score = {middleScore}') #report

    if lower <= 0:
        lowerScore += 10
        goodThings.append('There are enough lower order batsmen') #report
    else:
        lowerScore += 10 - (2*lowerScore) + (-1*recmiddle)
        badThings.append(f'There are not enough lower order batsmen hence lower score = {lowerScore}') #report

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
        goodThings.append('There are enough open bowlers') #report
    else:
        openscore += 10 - (3*recOpen)
        badThings.append('There are not enough new bowlers') #report
    
    if recChange <= 0:
        changescore += 10
        goodThings.append('There are enough change bowlers') #report
    else:
        changescore += 10 - (2*recChange) + (1*recOpen)        
        badThings.append('there are not enough change bowlers') #report
    
    if recDeath <= 0:
        deathscore += 10
        goodThings.append('There are enough death bowlers') #report
    elif recChange < 0:
        deathscore += 5
        badThings.append('there are not enough death bowlers can manage') #report
    else:
        badThings.append('not enough death bowlers and not enough change')
    
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
        goodThings.append('There are enough batsmen') #report
    else:
        batscore += 10 - abs(len(bat) - recBat)
        badThings.append("There are not enough Batsmen") #report
    
    batscore += judgeBatting(bat)
    
    if len(bowl) > minBowl:
        bowlscore += 10
        goodThings.append('There are enough bowlers') #report
    else:
        bowlscore += 10 - abs(len(bowl) - recBowl)
        badThings.append("There are not enough bowlers") #report
    
    bowlscore += judgebowling(bowl)
    
    if len(keep) < minKeep:
        keepscore += 0
    else:
        keepscore += 10

    print(f' bat = {batscore}, bowl = {bowlscore}, keep = {keepscore}') #debugging
    percentage = ((batscore + keepscore + bowlscore)/90) * 100
    percentage = round(percentage, 2)
    print(percentage) #debugging

    return percentage

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
        
        role = db.playerInfo(player,'role')

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
        team1str += battingStrength(batter,bowl2)
    
    for batter in bat2:
        team2str += battingStrength(batter,bowl1)
    
    finalScore = team1str - team2str
    
    return finalScore


def testFuntion():
    team1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    judgeTeam(team1)

testFuntion()
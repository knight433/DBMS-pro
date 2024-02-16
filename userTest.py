from cmath import rect
from numpy import rec

from sympy import O
import sqlQuer

db = sqlQuer.Database()

#database.addPlayer('virat Kholi',10,'batsman','RCB', 'right-arm pace','right')

battingdic = {
    'runs_to_Lspin' : 1155,
    'runs_to_Rspin' : 2598,
    'runs_to_Rpace' : 4163,
    'runs_to_Lpace' : 1344,
    'out_to_Lspin'  : 12,
    'out_to_Rspin'  : 24,
    'out_to_Rpace'  : 6,
    'out_to_Lpace'  : 15,
    'balls_Lspin'   : 902,
    'balls_Rspin'   : 945,
    'balls_Rpace'   : 1564,
    'balls_Lpace'   : 985,
    'pos' : 'top',
    'inng' : 60,
    'best' : 123
}

bowlingdic = {
    'runs_to_right'   : 45,
    'runs_to_left'    : 90,
    'wickets_to_right': 12,
    'wickets_to_left' : 2,
    'balls_to_right'  : 40,
    'balls_to_left'   : 53,
    'inngs'           : 26,
    'best'            : '2/12',
    'pos'             : 'second_change'
}

# database.addPlayer('virat Kholi',10,'batsman','RCB', 'right-arm pace','right',battingdic,bowlingdic)

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
        pos = db.getBattingInfo(bowler)

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





def testFuntion():
    a = db.getbowlinInfo(1,'prefered_bowler')
    print(a)

testFuntion()
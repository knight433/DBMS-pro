import sqlQuer

database = sqlQuer.Database()

#database.addPlayer('virat Kholi',10,'batsman','RCB', 'right-arm pace','right')

battingdic = {
    'runs_to_Lspin' : 1203,
    'runs_to_Rspin' : 1353,
    'runs_to_Rpace' : 2312,
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

def batsmenStrengthCount(batter_id,team):

    batterStrength = database.getBattingInfo(batter_id,'prefered_bowler')
    strCount = 0

    for player in team:

        role = database.playerRole(player)

        if role == "bowler" or role == "all-rounder":
            Btype = database.fetchBowlingType(player)  
            
            if batterStrength == Btype:
                strCount += 1

def bowlerStrengthCount(bowler_id,team):
    
    bowlerStrength = database.getbowlinInfo(bowler_id,'prefered_bowler')
    strCount = 0
    
    for player in team:
        role = database.playerRole(player)

        if role == 'batsmen' or role == 'all-rounder':
            
            hand = 0


def testFuntion():
    a = database.getbowlinInfo(1,'prefered_bowler')
    print(a)

testFuntion()
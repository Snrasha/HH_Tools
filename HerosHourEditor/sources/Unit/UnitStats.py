import math
import random


def roundGold(gold):
    return int(round(gold/5.))*5
def round2(val):
    return int(round(val/2.))*2
def calculateCost(rank):
    return round(15*(1+0.5*(rank**2)+0.1*(rank**3)))*5
def calculatePower(gold,rank,upgr):
    v = max(1,round(gold/75))
    if(v<10):
        v-=1
    if upgr:
        v = math.floor(v*1.15)
    if rank >= 5.5:
        v -= rank-4.5
    v -= math.floor((v-10)/ 5.)
    if v > 50:
        v = 50+(v-50)**.75
    if v >= 35:
        v=roundGold(v)
    elif v > 10:
        v=round2(v)
    return round(v)



def calculateGold(gold,percent,numberRes,res):
    goldUpgr=gold*percent
    goldUpgr=roundGold(goldUpgr)
    if(res=="L" or res=="O"):
        goldUpgr-=numberRes*100
    else:
        goldUpgr-=numberRes*200
    if(goldUpgr<0):
        goldUpgr=0
    return goldUpgr
        
    
def calculateRank(gold):
    rank=0
    cost=0
    while(gold>cost):
        cost=calculateCost(rank)
        rank+=0.01
    rank-=0.01

    diff1=abs(gold-cost)
    rank-=0.01
    cost=calculateCost(rank)
    diff2=abs(gold-cost)
    if(diff1<diff2):
        return rank+0.01
    else :
        return rank
def calculateRankStrength(rank):
    return (math.ceil(rank+1)+(max(rank,0)**1.25)*.8+2-rank/4)
def calculateHealth(rankStrength):
    return roundDec1(5*(rankStrength**1.5)+5)
def calculateDamage(rankStrength):
    return roundDec1(1.5*(rankStrength)+1)
def calculateSize(rank):
    return roundDec1(max(1,1+math.floor(rank*.6)/3))
def calculateAttackRange(size):
    return roundDec1(20*size)
def calculateSpeed(size):
    return roundDec1(20*size*.125)
def calculateWeight(rank):
    return abs(roundDec1(rank))

def roundDec1(v):
    return round(v,1)

##c=[75,85,120,185,285,425,615,855,1155,1520,1950,2455,3045,3720]
##for i in c:
##    rank=roundDec1(calculateRank(i))
##    print(str(rank)+";"+str(calculatePower(i,rank,False)))


def calculateAbilities(abilities,attackrange,weight,knockback,damage,health,speed,size):
    attackSpeed1="1.3s"
    attackSpeed2="(0% miss)"
    mspeed=1
    mhealth=1
    mdamage=1
    ranged=0
    for abi in abilities:
        abi=abi.lower()
        if(abi.startswith("windup")):
            attackSpeed2= "(50% miss)"
            mdamage *= 1.8
            mhealth *= 1.15
            continue
        if(abi.startswith("blaster")):
            attackrange+=96
            continue
        if(abi.startswith("flying")):
            mspeed+=1
            mdamage*=0.9
            mhealth*=.9
            continue
        if(abi.startswith("slow")):
            mspeed -= .3
            mhealth *= 1.15
            continue
        if(abi.startswith("tank")):
            mspeed-=0.3
            mhealth *= 1.5
            mdamage*=0.6
            continue
        if(abi.startswith("sturdy")):
            weight += 2
            mspeed -= .15
            mhealth *= 1.1
            mdamage *= .9
            continue
        if(abi.startswith("savage")):
            mhealth *= .75 
            mdamage *= 1.2 
            knockback+=1 
            continue
        if(abi.startswith("wide attacks")):
            mdamage *= .85
            mhealth *= .85
            continue
        if(abi.startswith("quick strikes")):
            attackSpeed1="0.75s"
            continue
        if(abi.startswith("knockback")):
            knockback += 2.5-1.5*ranged
            continue

        if(abi.startswith("ranged")):
            mhealth*=0.8
            mdamage*=1
            mspeed-=0.25
            weight-=1
            knockback-=1
            ranged=1
            attackrange=96+random.randint(0,64)
            continue
        if(abi.startswith("harpoonprojectile")):
            knockback+=2
            continue
        if(abi.startswith("small")):
            size=1
            weight-=1
            knockback-=1
            continue
        if(abi.startswith("big")):
            size+=1/3
            weight+=1
            knockback+=1
            continue
        if(abi.startswith("shrink")):
            size-=1/3
            continue
        if(abi.startswith("micro")):
            if(size>1):
                size=1
            else:
                size-=1/3
            continue
        if(abi.startswith("fast")):
            mdamage*=0.95
            mspeed+=.5
            mhealth*=.95
            continue
        if(abi.startswith("flimsy")):
            mspeed += .25 
            weight -= 2
            continue
        if(abi.startswith("feeble")):
            mdamage*=0.75
            continue
        if(abi.startswith("lash")):
            mdamage *= .85
            mhealth *= .85
            continue
        if(abi.startswith("ethereal")):
            mhealth *= .65
            continue
        if(abi.startswith("burst")):
            mdamage *= 1.5
            attackSpeed1="0s"
            continue
        if(abi.startswith("rebirth")):
            size -= 1/3
            knockback-=1
            weight-=1
            mhealth *= .7
            mdamage *= .8
            continue
        if(abi.startswith("immortal")):
            knockback-=1
            weight-=1
            mhealth *= .8
            mdamage *= .8
            continue

    return (attackSpeed1+attackSpeed2,roundDec1(attackrange),roundDec1(weight),roundDec1(knockback),damage*mdamage,health*mhealth,roundDec1(2*calculateSpeed(size)*mspeed),roundDec1(size))
        

##			case "Wide Attacks": atw += 3 ; damage *= .85 ; mhealth *= .85 ; addicon(mii_aoe,7) ; break; 
##			case "Lash": atw += 10 ; damage *= .85 ; mhealth *= .85 ; threeheaded = 1 ; addicon(mii_aoe,8) ; break; 
##			
##			case "Quick Strikes": matcd -= 2 ; addicon(mii_retaliation,12) ; break;	
##			case "Burst": baneling = 1 ; threeheaded = 1 ; atrange += 2 ; damage *= 1.5 ; atcd = 0 ; addicon(mii_aoe,35); break;##	
        
        
            
    


    
    
    

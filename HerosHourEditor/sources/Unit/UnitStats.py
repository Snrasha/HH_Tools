##cost = ROUND(15*(1+0.5*POWER(rank,2)+0.1*POWER(rank,3)))*5
##rankstrength = (min(rank+1)+power(max(rank,0),1.25)*.8+2-rank/4)*(upgr ? 1.16 : 1)
##damage = 1.5*rankstrength+1
##max health = 5*power(rankstrength,1.5)+5
##weight = rank
##attack power = rank
##size = max(1,1+floor(rank*.6)/3)
##attackrange = 20*size
##speed = 20*size*.125

import math
import random


def roundGold(gold):
    return int(round(gold/5.))*5
def round2(val):
    return int(round(gold/2.))*2
def calculateCost(rank):
    return round(15*(1+0.5*(rank**2)+0.1*(rank**3)))*5
def calculatePower(gold,rank,upgr):
    v = max(1,round(gold/75))
    if upgr:
        v = math.floor(v*1.15)
    if rank >= 5.5:
        v -= rank-4.5
    v -= (v-10)/ 5
    if v > 50:
        v = 50+(v-50)**.75
    if v >= 35:
        v=roundGold(v)
    elif v > 10:
        v=round2(v)
    return(v)

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
    

##def calculatePower(rank):
##    return (math.ceil(rank)*1.5+2)

def calculateAbilities(abilities,attackrange,weight,knockback,damage,health,speed,size):
    attackSpeed1="1.3s"
    attackSpeed2="(0% miss)"
    mspeed=1
    mhealth=1
    mdamage=1
    ranged=0
    for abi in abilities:
        if(abi.startswith("Windup")):
            attackSpeed2= "(50% miss)"
            mdamage *= 1.8
            mhealth *= 1.15
            continue
        if(abi.startswith("Blaster")):
            attackrange+=96
            continue
        if(abi.startswith("Flying")):
            mspeed+=1
            mdamage*=0.9
            mhealth*=.9
            continue
        if(abi.startswith("Slow")):
            mspeed -= .3
            mhealth *= 1.15
            continue
        if(abi.startswith("Tank")):
            mspeed-=0.3
            mhealth *= 1.5
            mdamage*=0.6
            continue
        if(abi.startswith("Sturdy")):
            weight += 2
            mspeed -= .15
            mhealth *= 1.1
            mdamage *= .9
            continue
        if(abi.startswith("Savage")):
            mhealth *= .75 
            mdamage *= 1.2 
            knockback+=1 
            continue
        if(abi.startswith("Wide Attacks")):
            mdamage *= .85
            mhealth *= .85
            continue
        if(abi.startswith("Quick Strikes")):
            attackSpeed1="0.75s"
            continue
        if(abi.startswith("Knockback")):
            knockback += 2.5-1.5*ranged
            continue
        if(abi.startswith("Ranged")):
            mhealth*=0.8
            mdamage*=1
            mspeed-=0.25
            weight-=1
            knockback-=1
            ranged=1
            attackrange=96+random.randint(0,64)
            continue
        if(abi.startswith("Harpoonprojectile")):
            knockback+=2
            continue
        if(abi.startswith("Small")):
            size=3
            weight-=1
            knockback-=1
            continue
        if(abi.startswith("Big")):
            size+=1
            weight+=1
            knockback+=1
            continue
        if(abi.startswith("Shrink")):
            size-=1
            continue
        if(abi.startswith("Micro")):
            if(size>3):
                size=3
            else:
                size-=1
            continue
        if(abi.startswith("Fast")):
            mdamage*=0.95
            mspeed+=.5
            mhealth*=.95
            continue
        if(abi.startswith("Flimsy")):
            mspeed += .25 
            weight -= 2
            continue
        if(abi.startswith("Feeble")):
            mdamage*=0.75
            continue
        if(abi.startswith("Lash")):
            mdamage *= .85
            mhealth *= .85
            continue
        if(abi.startswith("Ethereal")):
            mhealth *= .65
            continue
        if(abi.startswith("Burst")):
            mdamage *= 1.5
            attackSpeed1="0s"
            continue
        if(abi.startswith("Rebirth")):
            size -= 1
            knockback-=1
            weight-=1
            mhealth *= .7
            mdamage *= .8
            continue
        if(abi.startswith("Immortal")):
            knockback-=1
            weight-=1
            mhealth *= .8
            mdamage *= .8
            continue             
            
    return (attackSpeed1+attackSpeed2,roundDec1(attackrange),roundDec1(weight),roundDec1(knockback),damage*mdamage,health*mhealth,roundDec1(speed*mspeed),roundDec1(size))
        

##			case "Wide Attacks": atw += 3 ; damage *= .85 ; mhealth *= .85 ; addicon(mii_aoe,7) ; break; 
##			case "Lash": atw += 10 ; damage *= .85 ; mhealth *= .85 ; threeheaded = 1 ; addicon(mii_aoe,8) ; break; 
##			
##			case "Quick Strikes": matcd -= 2 ; addicon(mii_retaliation,12) ; break;	
##			case "Burst": baneling = 1 ; threeheaded = 1 ; atrange += 2 ; damage *= 1.5 ; atcd = 0 ; addicon(mii_aoe,35); break;##	
        
        
            
    


    
    
    

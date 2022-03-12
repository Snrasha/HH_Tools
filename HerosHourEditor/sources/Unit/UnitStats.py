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
def calculateCost(rank):
    return round(15*(1+0.5*(rank**2)+0.1*(rank**3)))*5
    
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
    return round(5*(rankStrength**1.5)+5,1)
def calculateDamage(rankStrength):
    return round(1.5*(rankStrength)+1,1)
def calculateSize(rank):
    return round(max(1,1+math.floor(rank*.6)/3),1)
def calculateAttackRange(size):
    return round(20*size,1)
def calculateSpeed(size):
    return round(20*size*.125,1)
def calculateWeight(rank):
    return abs(round(rank,1))

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
            
    return (attackSpeed1+attackSpeed2,attackrange,weight,knockback,damage*mdamage,health*mhealth,speed*mspeed,size)
        

##			case "Wide Attacks": atw += 3 ; damage *= .85 ; mhealth *= .85 ; addicon(mii_aoe,7) ; break; 
##			case "Lash": atw += 10 ; damage *= .85 ; mhealth *= .85 ; threeheaded = 1 ; addicon(mii_aoe,8) ; break; 
##			
##			case "Quick Strikes": matcd -= 2 ; addicon(mii_retaliation,12) ; break;	
##			case "Burst": baneling = 1 ; threeheaded = 1 ; atrange += 2 ; damage *= 1.5 ; atcd = 0 ; addicon(mii_aoe,35); break;##	
        
        
            
    


    
    
    

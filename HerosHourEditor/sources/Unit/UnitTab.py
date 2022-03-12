import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image,ImageTk
import Utils
import Utils.CommonClass as CommonClass
import Utils.CommonFunctions as CommonFunctions
import Utils.ToolTipFactory as ToolTipFactory
import Unit.UnitUtils as UnitUtils
import Unit.UnitStats as UnitStats


fields=["Names","Gold cost for base unit","Weekly Growth",
        "Rare Resource Cost","Balance modifier","Abilities for base unit",
        "Abilities for upgrade","Use sound effects from X unit","Attack type",
        "Living","Link","Unit groups"
        ]
fieldsUp=['NAMES', 'GOLD COST FOR BASE UNIT', 'WEEKLY GROWTH', 'RARE RESOURCE COST', 'BALANCE MODIFIER', 'ABILITIES FOR BASE UNIT',
 'ABILITIES FOR UPGRADE', 'USE SOUND EFFECTS FROM X UNIT', 'ATTACK TYPE', 'LIVING', 'LINK', 'UNIT GROUPS']

rareResource={"Ore":"O", "Lumber":"L", "Sulphur":"S", "Crystal":"C","Mercury":"M"}
rareResourceEdit={"O":"Ore","L": "Lumber", "S":"Sulphur", "C":"Crystal","M":"Mercury"}

rareResourceNumber=["0","1","2","3","4","5","6","7","8","9"]

attackType=["0: defensive","1: aggressive","2: magical"]
living=["-2: blight","-1: undead","0: elemental","1: living","2: humanoid","3: beast"]
descLiving="Specify whether the unit should be considered undead, constructed, living, etc"
descAttack="No difference currently for aggressive and defensive. Magical is for the Hero Potency Skill"

tooltipRareRes="Rare resource cost when you buy a unit\nDecrease gold cost except when you can buy only with gold"

tooltipSound="Press F+X in the HH main menu to bring up the list of all sounds"
tooltipLink="Unit summoned via Summoning, Bodyguards, or similar"

class TabUnitEditor(CommonClass.Tab):
    def  __init__(self,master,window,**kwargs):
        CommonClass.Tab.__init__(self,master,window,**kwargs)
        self.pack(fill=tk.BOTH,expand=True)
        self.master=master
        self.filename=None

        style = ttk.Style(self)
        self.bg = style.lookup('TFrame', 'background')

        self.initStandardField()
        
        self.initMiddleFrame()

        self.initRightFrame()
        self.updateStats()

    def initMiddleFrame(self):
        middleFrame=ttk.Frame(self)
        middleFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1),expand=True)
        frame0=ttk.LabelFrame(middleFrame,text='Unit cost')
        frame0.pack(fill=tk.BOTH,side=tk.TOP)
        frame=ttk.Frame(frame0)
        frame.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor="n")
        frame1=ttk.Frame(frame0)
        frame1.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor="n")        
        self.centerFieldsEntry=[]
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.centerFieldsEntry+=[CommonClass.Field(frame,titleField="Gold cost: ",hintField="100",side=tk.LEFT,width=10)]
        self.centerFieldsEntry[-1].entry.configure( validate = 'key',validatecommand = vcmd)

        self.centerFieldsEntry+=[CommonClass.Field(frame,titleField="Weekly Growth: ",hintField="30",command=self.updateStats,side=tk.LEFT,width=10)]
        self.centerFieldsEntry[-1].entry.configure( validate = 'key',validatecommand = vcmd)
##        self.centerFieldsEntry+=[CommonClass.OptionMenu(leftFrame,"Living:",living,descLiving)]
        self.centerFieldsEntry+=[CommonClass.OptionMenu(frame1,"Rare resource: ",rareResourceNumber,tooltipRareRes,command=self.updateStats,side=tk.LEFT)]
        self.centerFieldsEntry+=[CommonClass.OptionMenu(frame1,None,rareResource,tooltipRareRes,side=tk.LEFT)]


        frameStat=ttk.LabelFrame(middleFrame,text='Stats')
        frameStat.pack(fill=tk.BOTH,side=tk.TOP)
        frame1=ttk.Frame(frameStat)
        frame1.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor="n")
       
        self.centerFieldsEntry+=[CommonClass.Field(frame1,titleField="Balance modifier: ",hintField="100",side=tk.LEFT,width=10)]
        self.centerFieldsEntry[-1].entry.configure( validate = 'key',validatecommand = vcmd)
        ToolTipFactory.CreateToolTip(self.centerFieldsEntry[-1].entry, text = "version 2.0.5 and before, balance modifier are wrong. See modding guide")
        self.centerFieldsEntry+=[CommonClass.Field(frame1,titleField=None,hintField="100",side=tk.LEFT,width=10)]
        self.centerFieldsEntry[-1].entry.configure( validate = 'key',validatecommand = vcmd)
        ToolTipFactory.CreateToolTip(self.centerFieldsEntry[-1].entry, text = "version 2.0.5 and before, balance modifier are wrong. See modding guide")

        self.centerFieldsEntry+=[CommonClass.Field(frame1,titleField="Gold upgrade cost: ",hintField="35",side=tk.LEFT,width=10)]
        self.centerFieldsEntry[-1].entry.configure( validate = 'key',validatecommand = vcmd)
        ToolTipFactory.CreateToolTip(self.centerFieldsEntry[-1].entry, text = "Always 35% except Colony mod which is 50%")

        widthLabel=15
        
        frame2=ttk.Frame(frameStat,padding=(5,0))
        frame2.pack(side=tk.TOP,padx=(1,1),pady=(1,0),anchor="n")
        self.labels=[]
        for i in range(5):
            label=CommonClass.LabelSimplified(frame2,relief=tk.SUNKEN,borderwidth=1,width=widthLabel,anchor="center")
            label.pack(side=tk.LEFT,fill=tk.BOTH)
            self.labels+=[label]
        

        self.labels[0].set("Power")
        self.labels[1].set("Damage")
        self.labels[2].set("Health")
        self.labels[3].set("Size")
        self.labels[4].set("Speed")
        frame3=ttk.Frame(frameStat,padding=(5,0))
        frame3.pack(side=tk.TOP,padx=(1,1),pady=(0,1),anchor="n")
        frame4=ttk.Frame(frameStat,padding=(5,0))
        frame4.pack(side=tk.TOP,padx=(1,1),pady=(0,1),anchor="n")
        self.labelsStats=[]
        self.labelsStatsUpgraded=[]
        for i in range(5):
            label=CommonClass.LabelSimplified(frame3,relief=tk.SUNKEN,borderwidth=1,width=widthLabel,anchor="center")
            label.pack(side=tk.LEFT,fill=tk.BOTH)
            label.set("0")
            self.labelsStats+=[label]
        for i in range(5):
            label=CommonClass.LabelSimplified(frame4,relief=tk.SUNKEN,borderwidth=1,width=widthLabel,anchor="center")
            label.pack(side=tk.LEFT,fill=tk.BOTH)
            label.set("0")
            self.labelsStatsUpgraded+=[label]

        frame2=ttk.Frame(frameStat,padding=(5,0))
        frame2.pack(side=tk.TOP,padx=(1,1),pady=(1,0),anchor="n")
        for i in range(5):
            label=CommonClass.LabelSimplified(frame2,relief=tk.SUNKEN,borderwidth=1,width=widthLabel,anchor="center")
            label.pack(side=tk.LEFT,fill=tk.BOTH)
            self.labels+=[label]
        self.labels[6].set("Gold")
        self.labels[5].set("Weight")
        self.labels[7].set("Attack Speed")
        self.labels[8].set("Attack Range")
        self.labels[9].set("Knockback")
        
        frame3=ttk.Frame(frameStat,padding=(5,0))
        frame3.pack(side=tk.TOP,padx=(1,1),pady=(0,1),anchor="n")
        frame4=ttk.Frame(frameStat,padding=(5,0))
        frame4.pack(side=tk.TOP,padx=(1,1),pady=(0,1),anchor="n")

        for i in range(5):
            label=CommonClass.LabelSimplified(frame3,relief=tk.SUNKEN,borderwidth=1,width=widthLabel,anchor="center")
            label.pack(side=tk.LEFT,fill=tk.BOTH)
            label.set("0")
            self.labelsStats+=[label]
        for i in range(5):
            label=CommonClass.LabelSimplified(frame4,relief=tk.SUNKEN,borderwidth=1,width=widthLabel,anchor="center")
            label.pack(side=tk.LEFT,fill=tk.BOTH)
            label.set("0")
            self.labelsStatsUpgraded+=[label]

        
        
    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        
        if action == 0:
            return True
        if value_if_allowed == "":
            return True
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    def toInt(self,value):
        if(value==None or value ==""):
            return 1
        else:
            return int(value)
        
    def updateStats(self,event=None):
        attacktype,attacktypeUpgr=self.specialsFieldsEntry[0].getParams()
        
        abilities,abilitiesUpgr=self.specialsFieldsEntry[2].getParams()
        abilities=UnitUtils.getAttackRangeList(attacktype)+abilities
        abilitiesUpgr=UnitUtils.getAttackRangeList(attacktypeUpgr)+abilitiesUpgr

        abilitiesBis,abilitiesUpgrBis=self.specialsFieldsEntry[3].getParams()
        abilities+=abilitiesBis
        abilitiesUpgr+=abilitiesUpgrBis

        gold=self.toInt(self.centerFieldsEntry[0].get())
        gold=UnitStats.roundGold(gold)
        self.centerFieldsEntry[0].set(gold)

        

        rank=UnitStats.calculateRank(gold)
        
        balanceStat1=self.toInt(self.centerFieldsEntry[4].get())/100.
        balanceStat2=self.toInt(self.centerFieldsEntry[5].get())/100.
        
        if(self.checkBoxVar[0].get()==1):
            balanceStat2*=0
        rankStrength=UnitStats.calculateRankStrength(rank)

        power=UnitStats.calculatePower(gold,rank,False)
        powerUpgr=UnitStats.calculatePower(gold,rank,True)

        damage=UnitStats.calculateDamage(rankStrength)*balanceStat1
        damageUpgr=UnitStats.calculateDamage(rankStrength*1.16)*balanceStat2
        health=UnitStats.calculateHealth(rankStrength)*balanceStat1
        healthUpgr=UnitStats.calculateHealth(rankStrength*1.16)*balanceStat2
        size=UnitStats.calculateSize(rank)
        sizeUpgr=UnitStats.calculateSize(rank)
        speed=UnitStats.calculateSpeed(size)
        speedUpgr=UnitStats.calculateSpeed(sizeUpgr)
        speed=UnitStats.calculateSpeed(size)
        speedUpgr=UnitStats.calculateSpeed(sizeUpgr)
        weight=UnitStats.calculateWeight(rank)
        weightUpgr=UnitStats.calculateWeight(rank)
        attackSpeed="1.3s"
        attackSpeedUpgr="1.3s"
        attackRange=UnitStats.calculateAttackRange(size)
        attackRangeUpgr=UnitStats.calculateAttackRange(sizeUpgr)
        knockback=weight
        knockbackUpgr=weightUpgr
        attackSpeed,attackRange,weight,knockback,damage,health,speed,size=UnitStats.calculateAbilities(abilities,attackRange,weight,knockback,damage,health,speed,size)
        attackSpeedUpgr,attackRangeUpgr,weightUpgr,knockbackUpgr,damageUpgr,healthUpgr,speedUpgr,sizeUpgr=UnitStats.calculateAbilities(abilitiesUpgr,attackRangeUpgr,weightUpgr,knockbackUpgr,damageUpgr,healthUpgr,speedUpgr,sizeUpgr)
        #Power
        self.labelsStats[0].set(str(power))
        self.labelsStatsUpgraded[0].set(str(powerUpgr)+"+")
        
        #Damage
        self.labelsStats[1].set(str(round(damage)))
        self.labelsStatsUpgraded[1].set(str(round(damageUpgr)))
        #Health
        self.labelsStats[2].set(str(round(health)))
        self.labelsStatsUpgraded[2].set(str(round(healthUpgr)))
        # Size
        self.labelsStats[3].set(str(size))
        self.labelsStatsUpgraded[3].set(str(sizeUpgr))
        # Speed
        self.labelsStats[4].set(str(speed))
        self.labelsStatsUpgraded[4].set(str(speedUpgr))
        # Weight
        self.labelsStats[5].set(str(weight))
        self.labelsStatsUpgraded[5].set(str(weightUpgr))
        # Gold
        gold2=UnitStats.calculateGold(gold,1,int(self.centerFieldsEntry[2].get()),rareResource[self.centerFieldsEntry[3].get()])
        goldUpgr=UnitStats.calculateGold(gold,1+int(self.centerFieldsEntry[6].get())/100,int(self.centerFieldsEntry[2].get()),rareResource[self.centerFieldsEntry[3].get()])
        
        self.labelsStats[6].set(str(gold2))
        self.labelsStatsUpgraded[6].set(str(goldUpgr))      
        # Attack Speed
        self.labelsStats[7].set(attackSpeed)
        self.labelsStatsUpgraded[7].set(attackSpeedUpgr)
        # Attack Range
        self.labelsStats[8].set(str(attackRange))
        self.labelsStatsUpgraded[8].set(str(attackRangeUpgr))
        # Knockback
        self.labelsStats[9].set(str(knockback))
        self.labelsStatsUpgraded[9].set(str(knockbackUpgr))

    def initRightFrame(self):
        rightFrame=ttk.Frame(self)
        rightFrame.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(1,1),pady=(1,1),anchor="n",expand=False)

        CommonClass.FileFrame(rightFrame,self,side=tk.TOP)

        subframe2=ttk.LabelFrame(rightFrame,text='Stuff', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        self.checkBoxVar=[tk.IntVar()]
        checkbutton = tk.Checkbutton(subframe2, text="Neutral",variable = self.checkBoxVar[0], onvalue = 1, offvalue = 0,bg=self.bg,command=self.onCheckBoxChange)
        checkbutton.pack(side=tk.TOP)

        self.framesUnit=[]
        self.framesUnitImage=[]
        self.framesUnitImage+=[ImageTk.PhotoImage(Image.new("RGBA", (48,48), (255,255,255,255)))]
        self.framesUnitImage+=[ImageTk.PhotoImage(Image.new("RGBA", (48,48), (255,255,255,255)))]


        self.framesUnit+= [ttk.Label(subframe2)]
        self.framesUnit[0].pack(side=tk.TOP)
        self.framesUnit+= [ttk.Label(subframe2)]
        self.framesUnit[1].pack(side=tk.TOP)
        self.loadImages("")

    def initStandardField(self):

        self.fieldsEntry=[]
        standardField=ttk.LabelFrame(self,text='Fields', padding=(5, 5))
        standardField.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))

        self.fieldsEntry+=[CommonClass.Field(standardField,titleField="Unit Name:",hintField="Calf")]
        self.fieldsEntry+=[CommonClass.Field(standardField,titleField="Upgrade Name:",hintField="Cow")]
        self.fieldsEntry+=[CommonClass.Field(standardField,titleField="Sound Effect from a Unit:",hintField="Golem")]
        ToolTipFactory.CreateToolTip(self.fieldsEntry[-1].entry, text = tooltipSound)
        self.fieldsEntry+=[CommonClass.OptionMenu(standardField,"Attack type:",attackType,descAttack)]
        self.fieldsEntry+=[CommonClass.OptionMenu(standardField,"Living:",living,descLiving)]
        self.fieldsEntry+=[CommonClass.Field(standardField,titleField="Link:",hintField="Toadfrog")]
        ToolTipFactory.CreateToolTip(self.fieldsEntry[-1].entry, text = tooltipLink)
        self.fieldsEntry+=[CommonClass.Field(standardField,titleField="Unit groups:",hintField="")]

        self.specialsFieldsEntry=[]
        
        self.specialsFieldsEntry+=[UnitUtils.FieldAttackRange(standardField,command=self.updateStats)]
        self.specialsFieldsEntry+=[UnitUtils.FieldSpell(standardField)]
        self.specialsFieldsEntry+=[UnitUtils.FieldAbilities(standardField,command=self.updateStats)]
        self.specialsFieldsEntry+=[UnitUtils.FieldAbilitiesBis(standardField,command=self.updateStats)]

    def onCheckBoxChange(self):
        if(self.checkBoxVar[0].get()==0):
            self.fieldsEntry[1].entry.configure(state=tk.NORMAL)
            self.centerFieldsEntry[5].entry.configure(state=tk.NORMAL)
            self.centerFieldsEntry[1].entry.configure(state=tk.NORMAL)
            for i in range(2):
                self.centerFieldsEntry[i+2].optionMenu.configure(state=tk.NORMAL)
            for i in range(len(self.specialsFieldsEntry)):
                self.specialsFieldsEntry[i].setNeutral(0)
        else:
            self.fieldsEntry[1].entry.configure(state=tk.DISABLED)
            self.centerFieldsEntry[5].entry.configure(state=tk.DISABLED)
            self.centerFieldsEntry[1].entry.configure(state=tk.DISABLED)
            for i in range(2):
                self.centerFieldsEntry[i+2].optionMenu.configure(state=tk.DISABLED)
            for i in range(len(self.specialsFieldsEntry)):
                self.specialsFieldsEntry[i].setNeutral(1)
        self.updateStats()


    def loadImages(self,path):
        data=" data.txt"
        length=-len(data)
        if(data in path.lower()):
            path=path[:length]
        else:
            path=""
        self.addFrameUnit(path+" spritesheet.png",0)
        if(self.checkBoxVar[0].get()==0):
           self.addFrameUnit(path+"+ spritesheet.png",1)

        CommonFunctions.setImage(self.framesUnit[0],self.framesUnitImage[0],side=tk.LEFT)
        CommonFunctions.setImage(self.framesUnit[1],self.framesUnitImage[1],side=tk.LEFT)

    def addFrameUnit(self,pathUnit,i):
        gameImage=Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        if(os.path.exists(pathUnit)):
            image=Image.open(pathUnit)
            if(image.height>24):
                image=self.defaultImg()
            else:
                image=image.crop((0,0,image.height,image.height))
        else:
            image=self.defaultImg()
        gameImage.paste(image,box=(0,0,image.height,image.height))
        gameImage=gameImage.resize((48, 48),resample=Image.BOX)
        image = ImageTk.PhotoImage(gameImage)
        self.framesUnitImage[i]=image
    def defaultImg(self):
        return Image.new("RGBA", (24, 24), (0, 0, 0, 255))
    
    ## Open a existing file for edit it.
    def editFile(self):
        self.filename=CommonFunctions.askEditFile("Select a Unit file")
        if(self.filename==None):
            return None

        self.loadImages(self.filename)


        ## Made a backup of the opened file.
        CommonFunctions.madeBackUp("unit_backup.txt",self.filename)
        file1 = open(self.filename, 'r')
        self.lines=file1.readlines()
        self.count=0
        filled=[]
        listBaseAbilities=[]
        listUpgrAbilities=[]

        while self.count<len(self.lines):
            line=self.lines[self.count].strip()
            ## If found Name, check the next line. If the next line do not exist because it
            ## check than this is illegal, continue without increment.
            
            # NAMES
            if(line.upper().startswith(fieldsUp[0]) and fields[0] not in filled):
                filled+=[fields[0]]
                answer=self.getNextLine()
                self.fieldsEntry[0].set(answer)
                answer=self.getNextLine()
                if(answer!=None):
                    self.checkBoxVar[0].set(0)
                    self.fieldsEntry[1].set(answer)
                else:
                    self.checkBoxVar[0].set(1)
                    self.fieldsEntry[1].set("")
                continue
            # Gold cost for base unit
            if(line.upper().startswith(fieldsUp[1]) and fields[1] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.centerFieldsEntry[0].set(answer)
                    filled+=[fields[1]]
                continue
            # Weekly Growth
            if(line.upper().startswith(fieldsUp[2]) and fields[2] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.centerFieldsEntry[1].set(answer)
                    filled+=[fields[2]]
                continue
            # Rare Resource Cost
            if(line.upper().startswith(fieldsUp[3]) and fields[3] not in filled):
                answer=self.getNextLine()
                if(answer !=None and len(answer.strip())==2):
                    if(answer[1] in rareResourceEdit and answer[0] in rareResourceNumber):
                        self.centerFieldsEntry[2].set(answer[0])
                        self.centerFieldsEntry[3].set(rareResourceEdit[answer[1]])
                    else:
                        self.centerFieldsEntry[2].set("0")
                        self.centerFieldsEntry[3].set("Ore")
                    filled+=[fields[3]]
                continue
            # Balance modifier
            if(line.upper().startswith(fieldsUp[4]) and fields[4] not in filled):
                filled+=[fields[4]]
                answer=self.getNextLine()
                self.fieldsEntry[4].set(answer)
                answer=self.getNextLine()
                if(answer!=None):
                    self.checkBoxVar[0].set(0)
                    self.fieldsEntry[5].set(answer)
                else:
                    self.checkBoxVar[0].set(1)
                    self.fieldsEntry[5].set("100")
                continue
            # Abilities for base unit
            if(line.upper().startswith(fieldsUp[5]) and fields[5] not in filled):
                answer=self.getNextLine()
                filled+=[fields[5]]
                li=[]
                while(answer !=None):
                    li+=[answer]
                    answer=self.getNextLine()
                listBaseAbilities=li
                continue
            # Abilities for upgrade
            if(line.upper().startswith(fieldsUp[6]) and fields[6] not in filled):
                answer=self.getNextLine()
                filled+=[fields[6]]
                li=[]
                while(answer !=None):
                    li+=[answer]
                    answer=self.getNextLine()
                listUpgrAbilities=li

                continue
            
            # Use sound effects
            if(line.upper().startswith(fieldsUp[7]) and fields[7] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.fieldsEntry[2].set(answer)
                filled+=[fields[7]]
                continue
            # Attack type
            if(line.upper().startswith(fieldsUp[8]) and fields[8] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    for item in attackType:
                        if(item.startswith(answer)):
                            self.fieldsEntry[3].set(answer)
                filled+=[fields[8]]
                continue
            # Living
            if(line.upper().startswith(fieldsUp[9]) and fields[9] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    for item in living:
                        if(item.startswith(answer)):
                            self.fieldsEntry[4].set(answer)
                filled+=[fields[9]]
                continue
            # Link
            if(line.upper().startswith(fieldsUp[10]) and fields[10] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.fieldsEntry[5].set(answer)
                filled+=[fields[10]]
                continue
            # Unit groups
            if(line.upper().startswith(fieldsUp[11]) and fields[11] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.fieldsEntry[6].set(answer)
                filled+=[fields[11]]
                continue
            self.count+=1
        file1.close()

        self.specialsFieldsEntry[0].setParams(UnitUtils.loadAttackRange(listBaseAbilities),UnitUtils.loadAttackRange(listUpgrAbilities))
        self.specialsFieldsEntry[1].setParams(UnitUtils.loadSpell(listBaseAbilities),UnitUtils.loadSpell(listUpgrAbilities))
        self.specialsFieldsEntry[2].setParams(UnitUtils.loadStandardAbilities(listBaseAbilities),UnitUtils.loadStandardAbilities(listUpgrAbilities))
        self.specialsFieldsEntry[3].setParams(UnitUtils.loadAbilitiesBis(listBaseAbilities),UnitUtils.loadAbilitiesBis(listUpgrAbilities))

        self.updateStats()

    ## Found the next line to read. Ignore blank line except if stopToBlank is True
    def getNextLine(self):
        self.count+=1
        if(self.count<len(self.lines)):
            line=self.lines[self.count].strip()
            if(len(line)>0):
                
                return line
            else:
                return None
        return None

    ## Save a file. Check if all field are valid.
    def saveFile(self):
        self.filename=CommonFunctions.askSaveFile(self.filename,"Save Unit file")
        if(self.filename==None):
            self.filename=None
            return

        self.loadImages(self.filename)

        file1 = open(self.filename, 'w')
        inc=0
        notneutral= self.checkBoxVar[0].get()==0

        
        # Names
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[0].get().strip()+"\n")
        if(notneutral):
            file1.write(self.fieldsEntry[1].get().strip()+"\n")
        file1.write("\n")
        inc+=1

        # Gold cost
        file1.write(fields[inc]+"\n")
        file1.write(self.centerFieldsEntry[0].get().strip()+"\n\n")
        inc+=1

        if(notneutral):
            # weekly growth
            file1.write(fields[inc]+"\n")
            file1.write(self.centerFieldsEntry[1].get().strip()+"\n\n")
            # Rare resource
            file1.write(fields[inc+1]+"\n")
            file1.write(self.centerFieldsEntry[2].get().strip()+"")
            file1.write(rareResource[self.centerFieldsEntry[3].get()]+"\n\n")            
        inc+=2
        
        # Balance modifiers
        file1.write(fields[inc]+"\n")
        file1.write(self.centerFieldsEntry[4].get().strip()+"\n")
        if(notneutral):
            file1.write(self.centerFieldsEntry[5].get().strip()+"\n")
        file1.write("\n")
        inc+=1
        
        # Abilities
        attackrange,attackrangeUpgr=self.specialsFieldsEntry[0].getParams()
        spells,spellsUpgr=self.specialsFieldsEntry[1].getParams()
        abilities,abilitiesUpgr=self.specialsFieldsEntry[2].getParams()
        abilitiesBis,abilitiesUpgrBis=self.specialsFieldsEntry[3].getParams()

        file1.write(fields[inc]+"\n")
        inc+=1
        li=UnitUtils.getAttackRangeList(attackrange)
        li+=UnitUtils.getSpellList(spells)
        li+=abilities
        li+=abilitiesBis
        for item in li:
            file1.write(item+"\n")            
        file1.write("\n")
        
        if(notneutral):
            file1.write(fields[inc]+"\n")
            inc+=1
            li=UnitUtils.getAttackRangeList(attackrangeUpgr)
            li+=UnitUtils.getSpellList(spellsUpgr)
            li+=abilitiesUpgr
            li+=abilitiesUpgrBis
            for item in li:
                file1.write(item+"\n")
            file1.write("\n")

        # Sound
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[2].get().strip()+"\n\n")
        inc+=1
        # Attack type
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[3].get().strip().split(":")[0]+"\n\n")
        inc+=1
        # Living
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[4].get().strip().split(":")[0]+"\n\n")
        inc+=1
        # Link
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[5].get().strip()+"\n\n")
        inc+=1
        # Unit groups
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[6].get().strip()+"\n\n")
        inc+=1
        
        file1.close()
    
    def onKeyRelease(self,event):
        if(len(event.char)==1 and ord(event.char)==13 and CommonFunctions.checkIfInputField(type(self.oldFocus))):
            self.updateStats()
            return       
        
        self.oldFocus=self.focus_get()
         # If the user is on an entry / input field, skip the event.
        if(CommonFunctions.checkIfInputField(type(self.focus_get()))):

            return

        if(event.char=='d'):
            self.editFile()
        if(event.char=='v'):
            self.saveFile()

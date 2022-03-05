import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image,ImageTk
import Utils
import Utils.CommonClass as CommonClass
import Utils.CommonFunctions as CommonFunctions

fields=["FACTION NAME","FACTION UNITS ALTERNATES","HERO NAMES",
        "DWELLING NAMES","STARTING TERRAIN","TOWN NAMES",
        "HUMANOID ELITE TARGET","TOWN MUSIC","MAGIC SCHOOL SPECIALTY",
        "ARCHMAGE TRIBUNAL SKILL","LORE NAME","LORE MAIN RACE",
        "LORE HISTORY","LORE CULTURE","LORE HERO FIGHTER",
        "LORE HERO CASTER"
        ]

terrains=["Crag","Dirt","Grass","Ice","Lava","Swamp","Sand",
          "Deadlands","Moss Forest","Deep Forest","Tundra","Obsidian","Teal Marsh","Orange Desert"]

music=["Order", "Wild", "Arcane", "Decay", "Pyre", "Horde","Enclave", "Lament", "Tide", "Earthen"]

magic=["Water", "Air", "Fire", "Earth"]
humanoidEliteTarget=["1","2","3","4","5","6","7","8","9"]


descMagic="The guild of mages, archives of magic and archmage tribunal buildings in the town will offer different spells according to what element you specify here. For instance, if you pick fire, the three buildings will all be guaranteed to give a fire spell each, as well as teaching Fireskip and Rampaging Fire adventure map spells"
descMusic="Here you can specify what type of music should play when the player has the town screen open."
descTerrain="The starting terrain where you faction will start."
descHumanoidEliteTarget="Specific mechanics within the game require an elite humanoid target from each faction. It should be the highest tier humanoid unit the faction has - and if there’s just one or two humanoid units, you could pick one that isn’t."


class TabFactionEditor(CommonClass.Tab):     
    def  __init__(self,master,window,**kwargs):
        CommonClass.Tab.__init__(self,master,window,**kwargs)
        self.pack(fill=tk.BOTH,expand=True)
        self.master=master
        self.filename=None

        style = ttk.Style(self)
        self.bg = style.lookup('TFrame', 'background')

        self.initStandardField()

        middleFrame=ttk.Frame(self)
        middleFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1),expand=True)
        
        self.initContentFolder(middleFrame)

        self.initBuildings(middleFrame)

        rightFrame=ttk.Frame(self)
        rightFrame.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(1,1),pady=(1,1),anchor="n")
        
        CommonClass.FileFrame(rightFrame,self,side=tk.TOP)

        belowFrame=ttk.Frame(rightFrame,borderwidth=1,relief="sunken")
        belowFrame.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1),expand=True)

        self.saveInfo=CommonClass.LabelSimplified(belowFrame)
        self.saveInfo.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
        
    def initStandardField(self):
        
        self.fieldsEntry=[]
        standardField=ttk.LabelFrame(self,text='Fields', padding=(5, 5))
        standardField.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))
        
        self.canvas=tk.Canvas(standardField,bg=self.bg,relief=tk.FLAT,bd=0,highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)
        self.scrollbar1 = ttk.Scrollbar(standardField, orient='vertical', command=self.canvas.yview)
        self.scrollbar1.pack(fill=tk.Y,side=tk.LEFT,expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar1.set)

        leftFrame=ttk.Frame(self.canvas)
        leftFrame.pack(fill=tk.BOTH)



        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Faction name:",hintField="Kingdom")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Hero Name Fighter:",hintField="Fighter")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Hero Name Caster:",hintField="Caster")]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Starting Terrain:",listOfItems=terrains,description=descTerrain)]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Humanoid Elite Target:",listOfItems=humanoidEliteTarget,description=descHumanoidEliteTarget)]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Town Music:",listOfItems=music,description=descMusic)]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Magic School Specialty:",listOfItems=magic,description=descMagic)]

        self.skills=CommonFunctions.readSkills()
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Archmage Tribunal Skill:",listOfItems=self.skills.keys(),dictionnary=self.skills)]

        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Name:",hintField="Empire (not Order)")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Main Race:",hintField="Human")]
        self.fieldsEntry+=[CommonClass.FattyField(leftFrame,titleField="Lore History:",hintField="Bla bla genocide")]
        self.fieldsEntry+=[CommonClass.FattyField(leftFrame,titleField="Lore Culture:",hintField="Bla bla religion")]
        self.fieldsEntry+=[CommonClass.FattyField(leftFrame,titleField="Lore Hero Fighter:",hintField="Bla bla Inquisitor")]
        self.fieldsEntry+=[CommonClass.FattyField(leftFrame,titleField="Lore Hero Caster:",hintField="Bla bla Idol of death")]

        leftFrame.update_idletasks()
        self.canvas.create_window((0, 0), window=leftFrame, anchor='w')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.set_mousewheel(self.canvas)
        self.set_mousewheel(self.scrollbar1)
        

    def initContentFolder(self,middleFrame):
        contentFolder=ttk.LabelFrame(middleFrame,text='Folder Contents', padding=(5, 5))
        contentFolder.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1),expand=True)

        self.portraits=[]

        
        horFrame=ttk.Frame(contentFolder)
        horFrame.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        subhorFrame=ttk.Frame(horFrame,borderwidth=1,relief="sunken")
        subhorFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))
        label=ttk.Label(subhorFrame,text="Fighter: ")
        label.pack(fill=tk.BOTH,side=tk.LEFT)
        
        for i in range(0,3):
            self.portraits+=[ttk.Label(subhorFrame)]
            CommonFunctions.setBackground(self.portraits[i],48,side=tk.LEFT)
        subhorFrame=ttk.Frame(horFrame,borderwidth=1,relief="sunken")
        subhorFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))
        label=ttk.Label(subhorFrame,text="Caster: ")
        label.pack(fill=tk.BOTH,side=tk.LEFT)
        for i in range(3,6):
            self.portraits+=[ttk.Label(subhorFrame)]
            CommonFunctions.setBackground(self.portraits[i],48,side=tk.LEFT)
        subhorFrame=ttk.Frame(horFrame,borderwidth=1,relief="sunken")
        subhorFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))
        self.town=ttk.Label(subhorFrame)
        label=ttk.Label(subhorFrame,text="Town: ")
        label.pack(fill=tk.BOTH,side=tk.LEFT)
        CommonFunctions.setBackground(self.town,64,side=tk.LEFT)

    def initBuildings(self,middleFrame):
        buildFrame=ttk.LabelFrame(middleFrame,text='Buildings', padding=(5, 5))
        buildFrame.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1),expand=True)
        
        frames=[]
        self.buildings=[1,2,3]
        self.checkBoxVar=[]
        self.checkbuttons=[]

        self.tiersUnitLabel=[]
        self.tiersUnitImage=[]
        self.buildingsName=[]


        for i in range(6):
            self.checkBoxVar+=[tk.IntVar()]
            frame1=ttk.Frame(buildFrame)
            frame1.pack(side=tk.TOP,padx=(1,1),pady=(1,1))
            frames+=[frame1]

            self.buildingsName+=[CommonClass.EntrySimplified(frame1)]
            self.buildingsName[i].set("building "+str(i))
            self.buildingsName[i].pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))
            
            checkbutton = tk.Checkbutton(frame1, variable = self.checkBoxVar[i], onvalue = 1, offvalue = 0,bg=self.bg,command=self.onCheckBoxChange)
            checkbutton.pack(side=tk.LEFT)
            self.checkbuttons+=[checkbutton]
            if(i in self.buildings):
                self.checkBoxVar[i].set(1)
                self.checkbuttons[i].configure(state=tk.NORMAL)
            else:
                self.checkBoxVar[i].set(0)
                self.checkbuttons[i].configure(state=tk.DISABLED)

            self.tiersUnitLabel+=[ttk.Label(frame1)]
            self.tiersUnitLabel[i*2].pack(side=tk.LEFT)
            
            self.tiersUnitLabel+=[ttk.Label(frame1)]
            self.tiersUnitLabel[i*2+1].pack(side=tk.LEFT)


        for i in range(9):
            self.tiersUnitImage+=[ImageTk.PhotoImage(Image.new("RGBA", (48,24), (255,255,255,255)))]

        self.tiersUnitImage+=[ImageTk.PhotoImage(Image.new("RGBA", (48,24), (0,0,0,255)))]
        
        self.setTierUnit(self.buildings)               

            
                

    def setTierUnit(self,builds):
        inc=0
        for i in range(6):
            CommonFunctions.setImage(self.tiersUnitLabel[i*2],self.tiersUnitImage[inc],side=tk.LEFT)
            if i in builds:
                inc+=1
                CommonFunctions.setImage(self.tiersUnitLabel[i*2+1],self.tiersUnitImage[inc],side=tk.LEFT)
            else:
                CommonFunctions.setImage(self.tiersUnitLabel[i*2+1],self.tiersUnitImage[-1],side=tk.LEFT)
            inc+=1

        
    def onCheckBoxChange(self):
        build=[]
        for i in range(6):
            
            if(self.checkBoxVar[i].get()==1):
                build+=[i]
        self.setTierUnit(build)

        if(len(build) >=3):
            for i in range(6):
                if(i in build):
                    self.checkbuttons[i].configure(state=tk.NORMAL)
                else:
                    self.checkbuttons[i].configure(state=tk.DISABLED)
            if(len(build)==3):
                self.buildings=build
                return
        else:
            for i in range(6):
                self.checkbuttons[i].configure(state=tk.NORMAL)

        # Will stop the save if the building is "empty" because less than 3 or more than 3 checked.
        self.buildings=None

    
    def set_mousewheel(self,widget):
        """Activate / deactivate mousewheel scrolling when 
        cursor is over / not over the widget respectively."""
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', self.onMouseWheel))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

    def onMouseWheel(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def loadImages(self,path):
        data="faction.txt"
        length=-len(data)
        
        if(data in path.lower()):
            pathDir=path[:length]+"Folder/"
        else:
            pathDir=""
####        if not (os.path.exists(pathDir)):
##            CommonClass.Popup("faction Folder do not exist. Verify it. This is case-sensitive")
            

        for i in range (6):
            path=pathDir+"Hero "+str(i+1)
            if(os.path.exists(path+" data.txt")):
                path=path+" portrait.png"
                CommonFunctions.addImage(path,self.portraits[i],48,True,tk.LEFT)
            else:
                CommonFunctions.setBackground(self.portraits[i],48,side=tk.LEFT)
        for i in range (9):
            path=pathDir+"Unit "+str(i+1)+" spritesheet.png"
            path2=pathDir+"Unit "+str(i+1)+"+ spritesheet.png"
            self.addFrameUnits(path,path2,i)       
                       
    def addFrameUnits(self,pathUnit,pathUnitUpgraded,i):
        gameImage=Image.new("RGBA", (48, 24), (0, 0, 0, 0))
        if(os.path.exists(pathUnit)):
            image=Image.open(pathUnit)
            if(image.height>24):
                image=self.defaultImg()
            else:
                image=image.crop((0,0,image.height,image.height))
        else:
            image=self.defaultImg()
        gameImage.paste(image,box=(0,0,image.height,image.height))
        if(os.path.exists(pathUnitUpgraded)):
            image=Image.open(pathUnitUpgraded)
            if(image.height>24):
                image=self.defaultImg()
            else:
                image=image.crop((0,0,image.height,image.height))
        else:
            image=self.defaultImg()
        gameImage.paste(image,box=(image.height,0,image.height*2,image.height))
        image = ImageTk.PhotoImage(gameImage)
        self.tiersUnitImage[i]=image
    def defaultImg(self):
        return Image.new("RGBA", (24, 24), (0, 0, 0, 255))
        

    ## Open a existing file for edit it.
    def editFile(self):
        self.filename=CommonFunctions.askEditFile("Select a Faction file")
        if(self.filename==None):
            return None

        self.loadImages(self.filename)
        
##        for field in self.fieldsEntry:
##            field.empty()
        
        ## Made a backup of the opened file.
        CommonFunctions.madeBackUp("faction_backup.txt",self.filename)
        file1 = open(self.filename, 'r')
        self.lines=file1.readlines()
        self.count=0
        filled=[]

        verySimpleField=[0,10,11,12,13,14,15]
        verySimpleField2=[0,8,9,10,11,12,13]
        
        
        while self.count<len(self.lines):
            line=self.lines[self.count].strip()
            
            ## If found Name, check the next line. If the next line do not exist because it
            ## check than this is illegal, continue without increment.

            # FACTION NAME,"LORE NAME","LORE MAIN RACE","LORE HISTORY","LORE CULTURE","LORE HERO FIGHTER", "LORE HERO CASTER"
            for i in range(len(verySimpleField)):
                t=verySimpleField[i]
                if(line.upper().startswith(fields[t]) and fields[t] not in filled):
                    answer=self.getNextLine()
                    if(answer !=None):
                        self.fieldsEntry[verySimpleField2[i]].set(answer)
                        filled+=[fields[t]]
                    continue
            ## FACTION UNITS ALTERNATES
            if(line.upper().startswith(fields[1])):
                answer=self.getNextLine()
                filled+=[fields[1]]
                
                for i in range(6):
                    self.checkBoxVar[i].set(0)
                
                while(answer !=None):
                    print(answer)
                    try:
                        ans=int(answer)
                        self.checkBoxVar[ans-1].set(1)
                    except:
                        self.onCheckBoxChange()
                        continue
                    answer=self.getNextLine()
                else:
                    self.onCheckBoxChange()
                    continue
            
            # HERO NAMES
            if(line.upper().startswith(fields[2]) and fields[2] not in filled):
                filled+=[fields[2]]
                answer=self.getNextLine()
                self.fieldsEntry[1].set(answer)
                answer=self.getNextLine()
                self.fieldsEntry[2].set(answer)
                continue
            # DWELLING NAMES
            if(line.upper().startswith(fields[3]) and fields[3] not in filled):
                answer=self.getNextLine()
                filled+=[fields[3]]
                inc=0
                while(answer !=None and inc < 6):
                    
                    self.buildingsName[inc].set(answer)
                    answer=self.getNextLine()
                    inc+=1
                continue
            # STARTING TERRAIN
            if(line.upper().startswith(fields[4]) and fields[4] not in filled):
                answer=self.getNextLine()
                if(answer in terrains):
                    self.fieldsEntry[3].set(answer)
                else:
                    self.fieldsEntry[3].set(terrains[0])
                filled+=[fields[4]]
                continue
            # TOWN NAMES
            if(line.upper().startswith(fields[5]) and fields[5] not in filled):
                answer=self.getNextLine()
                filled+=[fields[5]]
                while(answer !=None):
                    answer=self.getNextLine()
                continue
            # HUMANOID ELITE TARGET
            if(line.upper().startswith(fields[6]) and fields[6] not in filled):
                answer=self.getNextLine()
                if(answer in humanoidEliteTarget):
                    self.fieldsEntry[4].set(answer)
                else:
                    self.fieldsEntry[4].set(humanoidEliteTarget[0])
                filled+=[fields[6]]
                continue
            # TOWN MUSIC
            if(line.upper().startswith(fields[7]) and fields[7] not in filled):
                answer=self.getNextLine()
                if(answer in music):
                    self.fieldsEntry[5].set(answer)
                else:
                    self.fieldsEntry[5].set(music[0])
                filled+=[fields[7]]
                continue
            # MAGIC SCHOOL SPECIALTY
            if(line.upper().startswith(fields[8]) and fields[8] not in filled):
                answer=self.getNextLine()
                if(answer in magic):
                    self.fieldsEntry[6].set(answer)
                else:
                    self.fieldsEntry[6].set(magic[0])
                filled+=[fields[8]]
                continue
            # ARCHMAGE TRIBUNAL SKILL
            if(line.upper().startswith(fields[9]) and fields[9] not in filled):
                answer=self.getNextLine()
                if(answer in self.skills):
                    self.fieldsEntry[7].set(answer)
                else:
                    self.fieldsEntry[7].set("None")
                filled+=[fields[9]]
                continue
            self.count+=1
        file1.close()
        
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

        if(self.buildings==None or len(self.buildings)!=3):
            self.saveInfo.set("Unit alternate need to have 3 checkbox checked")
            return
        for i in range(6):
            if(len(self.buildingsName[i].get().strip())==0):
                self.saveInfo.set("Building name need one character minimum")
                return
            
        if(self.fieldsEntry[7].get()=='None'):
            self.saveInfo.set("Archmage Tribunal Skill need a skill")
            return            
        for field in self.fieldsEntry:
            if(field.get().strip()==0):
                self.saveInfo.set("One or more fields are empty")
                return

            
            
        
        self.filename=CommonFunctions.askSaveFile(self.filename,"Save Faction file")
        if(self.filename==None):
            self.filename=None
            return

        self.loadImages(self.filename)

        inc=0
        
        file1 = open(self.filename, 'w')
        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[0].get().strip()+"\n\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        for i in range(3):
            file1.write(str(self.buildings[i]+1)+"\n")
        file1.write("\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[1].get().strip()+"\n")
        file1.write(self.fieldsEntry[2].get().strip()+"\n\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        for i in range(0,6):
            file1.write(self.buildingsName[i].get().strip()+"\n")
        file1.write("\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[3].get().strip()+"\n\n")
        inc+=1

##        file1.write(fields[inc]+"\n")
##        for i in range(0,len(self.town_names)):
##            file1.write(self.town_names[i]+"\n")
##        file1.write("\n")
##        inc+=1

        for i in range(4,14):
            file1.write(fields[inc]+"\n")
            file1.write(self.fieldsEntry[i].get().strip()+"\n\n")
            inc+=1
            
        file1.close()
    def onKeyRelease(self,event):
         # If the user is on an entry / input field, skip the event.
        if(type(self.focus_get()) == tk.Entry or type(self.focus_get()) == ttk.Entry):
            return  
        
        if(event.char=='d'):
            self.editFile()
        if(event.char=='v'):
            self.saveFile()

        

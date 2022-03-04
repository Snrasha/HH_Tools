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

  
## Contains edit, save and the three simple fields.
class SimpleFields(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master,padx=5,pady=5)
        self.master=master
        self.filename=None

        CommonClass.FileFrame(self,side=tk.RIGHT,anchor="n")

        self.fieldsEntry=[]
        

        subframe2=ttk.LabelFrame(self,text='Fields', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1),expand=True)

        listFrame=tk.Frame(self)
        listFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))    


        self.pack(side=tk.LEFT,fill=tk.BOTH,expand=False)

        
        canvas=tk.Canvas(subframe2)
        canvas.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)
        scrollbar1 = ttk.Scrollbar(subframe2, orient='vertical', command=canvas.yview)
        scrollbar1.pack(fill=tk.Y,side=tk.LEFT,expand=True)
        canvas.configure(yscrollcommand=scrollbar1.set)

        leftFrame=tk.Frame(canvas)
        leftFrame.pack(fill=tk.BOTH)

        
        

        # 0 Name, 1 Unit, 2 Class
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Faction name:",hintField="")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Hero Name Fighter:",hintField="Fighter")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Hero Name Caster:",hintField="Caster")]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Starting Terrain:",listOfItems=terrains)]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Humanoid Elite Target:",hintField="9")]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Town Music:",listOfItems=music)]
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Magic School Specialty:",listOfItems=magic)]

        self.skills=CommonFunctions.readSkills()
        self.fieldsEntry+=[CommonClass.FieldList(leftFrame,titleField="Archmage Tribunal Skill:",listOfItems=self.skills.keys())]

        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Name:",hintField="Empire (not Order)")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Main Race:",hintField="Human")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore History:",hintField="Bla bla genocide")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Culture:",hintField="Bla bla religion")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Hero Fighter:",hintField="Bla bla Inquisitor")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Lore Hero Caster:",hintField="Bla bla Idol of death")]



        leftFrame.update_idletasks()
        canvas.create_window((0, 0), window=leftFrame, anchor='w')
        canvas.configure(scrollregion=canvas.bbox("all"))

    def loadImages(self,path):
        data="faction.txt"
        length=-len(data)
        
        if(data in path.lower()):
            pathDir=path[:length]+"Folder/"
        else:
            pathDir=""
        if not (os.path.exists(pathDir)):
            CommonClass.Popup("faction Folder do not exist. Verify it. This is case-sensitive")
            

        for i in range (6):
            path=pathDir+"Hero "+i+" portrait.png"
            CommonFunctions.addImage(path,self.portraits[i],48,outline=True)
        for i in range (9):
            path=pathDir+"Unit "+i+" spritesheet.png"
            path2=pathDir+"Unit "+i+"+ spritesheet.png"
            addFrameUnits(path,path2,self.unitsImg[i])          
                       
    def addFrameUnits(self,pathUnit,pathUnitUpgraded,label):
        gameImage=Image.new("RGBA", (48, 24), (0, 0, 0, 0))
        if(os.path.exists(pathUnit)):
            image=Image.open(pathUnit)
            image = ImageTk.PhotoImage(image)
        else:
            image=Image.new("RGBA", (24, 24), (0, 0, 0, 255))
        gameImage.paste(image,(0,24,0,24))
        if(os.path.exists(pathUnitUpgraded)):
            image=Image.open(pathUnitUpgraded)
            image = ImageTk.PhotoImage(image)
        else:
            image=Image.new("RGBA", (24, 24), (0, 0, 0, 255))
        gameImage.paste(image,(24,48,0,24))  
        

    ## Open a existing file for edit it.
    def editFile(self):
        self.filename=CommonFunctions.askEditFile("Select a Faction file")
        if(self.filename==None):
            return None

        self.loadImages(self.filename)
        
        for field in self.fieldsEntry:
            field.empty()
        
        ## Made a backup of the opened file.
        CommonFunctions.madeBackUp("faction_backup.txt",self.filename)
        file1 = open(self.filename, 'r')
        self.lines=file1.readlines()
        self.count=0
        filled=[]
        
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
        for i in range(0,3):
            file1.write(self.faction_unit_alternates[i]+"\n")
        file1.write("\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[1].get().strip()+"\n")
        file1.write(self.fieldsEntry[2].get().strip()+"\n\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        for i in range(0,6):
            file1.write(self.building_names[i]+"\n")
        file1.write("\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        file1.write(self.fieldsEntry[3].get().strip()+"\n\n")
        inc+=1

        file1.write(fields[inc]+"\n")
        for i in range(0,len(self.town_names)):
            file1.write(self.town_names[i]+"\n")
        file1.write("\n")
        inc+=1

        for i in range(4,15):
            file1.write(fields[inc]+"\n")
            file1.write(self.fieldsEntry[i].get().strip()+"\n\n")
            inc+=1
            
        file1.close()

class TabFactionEditor(CommonClass.Tab):     
    def  __init__(self,master,window):
        CommonClass.Tab.__init__(self,master,window)

        self.pack(fill=tk.BOTH,expand=True)
        self.simpleFields=SimpleFields(self)
        
    def onKeyRelease(self,event):
         # If the user is on an entry / input field, skip the event.
        if(type(self.focus_get()) == tk.Entry or type(self.focus_get()) == ttk.Entry):
            return  
        
        if(event.char=='d'):
            self.simpleFields.editFile()
        if(event.char=='v'):
            self.simpleFields.saveFile()
        

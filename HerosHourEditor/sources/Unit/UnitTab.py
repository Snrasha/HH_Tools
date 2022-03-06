import tkinter as tk
import tkinter.ttk as ttk
import os
from PIL import Image,ImageTk
import Utils
import Utils.CommonClass as CommonClass
import Utils.CommonFunctions as CommonFunctions
import Utils.ToolTipFactory as ToolTipFactory
fields=["Names","Gold cost for base unit","Weekly Growth",
        "Rare Resource Cost","Balance modifier","Abilities for base unit",
        "Abilities for upgrade","Use sound effects from X unit","Attack type",
        "Living","Link","Unit groups"
        ]


rareResource=["Ore", "Lumber", "Sulphur", "Crystal","Mercury"]
rareResourceId=["O", "L", "S", "C","M"]
rareResourceNumber=["0","1","2","3","4","5","6","7","8","9"]

attackType=["0: defensive","1: aggressive","2: magical"]
living=["-2: blight","-1: undead","0: elemental","1: living","2: humanoid","3: beast"]
descLiving="Specify whether the unit should be considered undead, constructed, living, etc"
descAttack="No difference currently for aggressive and defensive. Magical is for the Hero Potency Skill"

tooltipRareRes="Rare resource cost when you buy a unit"

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

    def initMiddleFrame(self):
        middleFrame=ttk.Frame(self)
        middleFrame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1),expand=True)
        frame0=ttk.LabelFrame(middleFrame,text='Unit cost')
        frame0.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        frame=ttk.Frame(frame0)
        frame.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        frame1=ttk.Frame(frame0)
        frame1.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))        
        self.centerFieldsEntry=[]
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.centerFieldsEntry+=[CommonClass.Field(frame,titleField="Gold cost:",hintField="100",side=tk.LEFT)]
        self.centerFieldsEntry[0].entry.configure( validate = 'key',validatecommand = vcmd)
##        self.centerFieldsEntry+=[CommonClass.OptionMenu(leftFrame,"Living:",living,descLiving)]
        self.centerFieldsEntry+=[CommonClass.OptionMenu(frame1,"Rare resource",rareResourceNumber,tooltipRareRes,side=tk.LEFT)]
        self.centerFieldsEntry+=[CommonClass.OptionMenu(frame1,None,rareResource,tooltipRareRes,side=tk.LEFT)]

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


    def initRightFrame(self):
        rightFrame=ttk.Frame(self)
        rightFrame.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(1,1),pady=(1,1),anchor="n")

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

        self.canvas=tk.Canvas(standardField,bg=self.bg,relief=tk.FLAT,bd=0,highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)
        self.scrollbar1 = ttk.Scrollbar(standardField, orient='vertical', command=self.canvas.yview)
        self.scrollbar1.pack(fill=tk.Y,side=tk.LEFT,expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar1.set)

        leftFrame=ttk.Frame(self.canvas)
        leftFrame.pack(fill=tk.BOTH)

##    fields=["Gold cost for base unit","Weekly Growth",
##            "Rare Resource Cost","Balance modifier","Abilities for base unit",
##            "Abilities for upgrade","Attack type",
##            "Living","Link","Unit groups"
##            ]

        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Unit Name:",hintField="Calf")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Upgrade Name:",hintField="Cow")]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Sound Effect from a Unit:",hintField="Golem")]
        ToolTipFactory.CreateToolTip(self.fieldsEntry[-1].entry, text = tooltipSound)
        self.fieldsEntry+=[CommonClass.OptionMenu(leftFrame,"Attack type:",attackType,descAttack)]
        self.fieldsEntry+=[CommonClass.OptionMenu(leftFrame,"Living:",living,descLiving)]
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Link:",hintField="Toadfrog")]
        ToolTipFactory.CreateToolTip(self.fieldsEntry[-1].entry, text = tooltipLink)
        self.fieldsEntry+=[CommonClass.Field(leftFrame,titleField="Unit groups:",hintField="")]
        

        leftFrame.update_idletasks()
        self.canvas.create_window((0, 0), window=leftFrame, anchor='w')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.set_mousewheel(self.canvas)
        self.set_mousewheel(self.scrollbar1)

        


    def onCheckBoxChange(self):
        if(self.checkBoxVar[0].get()==0):
            self.fieldsEntry[1].entry.configure(state=tk.NORMAL)
        else:
            self.fieldsEntry[1].entry.configure(state=tk.DISABLED)

    def set_mousewheel(self,widget):
        """Activate / deactivate mousewheel scrolling when
        cursor is over / not over the widget respectively."""
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', self.onMouseWheel))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))

    def onMouseWheel(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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

        CommonFunctions.setImage(self.framesUnit[0],self.framesUnitImage[0],side=tk.TOP)
        CommonFunctions.setImage(self.framesUnit[1],self.framesUnitImage[1],side=tk.TOP)

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

        ## Made a backup of the opened file.
        CommonFunctions.madeBackUp("unit_backup.txt",self.filename)
        file1 = open(self.filename, 'r')
        self.lines=file1.readlines()
        self.count=0
        filled=[]
        self.loadImages(self.filename)

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
        self.filename=CommonFunctions.askSaveFile(self.filename,"Save Unit file")
        if(self.filename==None):
            self.filename=None
            return

        self.loadImages(self.filename)

        file1 = open(self.filename, 'w')
        file1.close()
    def onKeyRelease(self,event):
         # If the user is on an entry / input field, skip the event.
        if(CommonFunctions.checkIfInputField(type(self.focus_get()))):
            return

        if(event.char=='d'):
            self.editFile()
        if(event.char=='v'):
            self.saveFile()

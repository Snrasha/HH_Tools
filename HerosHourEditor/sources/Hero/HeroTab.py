import tkinter as tk
import tkinter.ttk as ttk
import Hero.ListSearchBar as ListSearchBar
from PIL import Image,ImageTk
import Utils.CommonClass as CommonClass
import Utils.CommonFunctions as CommonFunctions


fields=["Name","Unit","Class","Skills"]

## Contains the search bar, the description (placed wrongly) and the skill tree.
class SkillFields(ttk.Frame):
    def  __init__(self,master):
        ttk.Frame.__init__(self,master)

        self.master=master
        self.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        subframe0=ttk.Frame(self,borderwidth=1,relief=tk.GROOVE)
        subframe0.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))

        self.currentSlot=None
        self.allSkills=[]

        style = ttk.Style(self)
        bg = style.lookup('TFrame', 'background')

##        style = ttk.Style(self)
##        style.configure('TLabelframe', background="white")

        self.searchBar=ListSearchBar.SearchBar(subframe0,self)



  

        frame_canvas = ttk.Frame(self)
        frame_canvas.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)
        canvas=tk.Canvas(frame_canvas,bg=bg,highlightthickness=0,relief=tk.FLAT,bd=0)
        canvas.pack(fill=tk.BOTH,side=tk.TOP, expand=True)       

        scrollbar2 = ttk.Scrollbar(frame_canvas, orient='horizontal', command=canvas.xview)
        scrollbar2.pack(fill=tk.X,side=tk.BOTTOM)
        canvas.configure(xscrollcommand=scrollbar2.set)
        scrollbar1 = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        scrollbar1.pack(fill=tk.Y,side=tk.RIGHT)
        canvas.configure(yscrollcommand=scrollbar1.set)
        frame_inner = ttk.Frame(canvas)
        frame_inner.pack(fill=tk.BOTH)        
        
        
        subframe2=ttk.LabelFrame(frame_inner,text='Skill Tree', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        subframe3=ttk.LabelFrame(frame_inner,text='Informations', padding=(5, 5))
        subframe3.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        subframe1=ttk.LabelFrame(frame_inner,text='Description Skill', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        self.labelDesc=ttk.Label(subframe1,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.TOP,fill=tk.X,padx=5,pady=5)
        
        self.labelDesc.configure(text=self.searchBar.descriptionsSkills["None"])
        
        self.portrait = ttk.Label(subframe3)
        self.portrait.pack()


        # Create 4 frame below each other. Centered North on the parent.
        level0=ttk.Frame(subframe2)
        level0.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor=tk.N)
        level1=ttk.Frame(subframe2)
        level1.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor=tk.N)
        level2=ttk.Frame(subframe2)
        level2.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor=tk.N)
        level3=ttk.Frame(subframe2)
        level3.pack(side=tk.TOP,padx=(1,1),pady=(1,1),anchor=tk.N)

        for i in range(0,2):
            self.createLabel(level0)
        for i in range(0,4):
            self.createLabel(level1)
        for i in range(0,5):
            self.createLabel(level2)
        for i in range(0,6):
            self.createLabel(level3)


            
        frame_inner.update_idletasks()
        subframe2.update()
        self.labelDesc.config(wraplength=(subframe2.winfo_width()*0.9))
        canvas.create_window((0, 0), window=frame_inner, anchor='w')
        canvas.configure(scrollregion=canvas.bbox("all"))
            
    def createLabel(self,frame):
        v = tk.StringVar()
        
        label=CommonClass.LabelSimplified(frame,padding=(2,2),background="white",width=20,borderwidth=1,relief=tk.SUNKEN)
        label.set("None")
        label.pack(side=tk.LEFT,padx=1,pady=1)
        label.bind("<Button-1>",self.onEnter)
        self.allSkills+=[label]

    def onEnter(self,event):
        if(self.currentSlot!=None):
            self.currentSlot.configure(background="white")
        self.currentSlot=event.widget
        self.labelDesc.configure(text=self.searchBar.descriptionsSkills[self.currentSlot.get()])
        self.currentSlot.configure(background="green")

    def setValue(self,value):
        if(self.currentSlot!=None):
            self.currentSlot.set(value)
            labels=self.allSkills
            for label in labels:
                if(label==self.currentSlot):
                    return
                if(label.get() == "None"):
                    label.configure(background="red")

                
## Contains edit, save and the three simple fields.
class SimpleFields(ttk.Frame):
    def  __init__(self,master):
        ttk.Frame.__init__(self,master)
        self.master=master
        self.filename=None

        self.fieldsEntry=[]
        style = ttk.Style(self)
        bg = style.lookup('TFrame', 'background')
        
        self.pack(side=tk.RIGHT,fill=tk.Y,expand=False)

        CommonClass.FileFrame(self,fill=tk.X)

        subframe2=ttk.LabelFrame(self,text='Fields', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        # 0 Name, 1 Unit, 2 Class
        self.fieldsEntry+=[CommonClass.Field(subframe2,titleField="Name:",hintField="Hero name",width=15)]
        self.fieldsEntry+=[CommonClass.Field(subframe2,titleField="Unit:",hintField="Starting Unit",width=15)]
        self.fieldsEntry+=[CommonClass.Field(subframe2,titleField="Class:",width=15)]
        
        self.checkBoxVar=[tk.IntVar(),tk.IntVar()]
        checkbutton = tk.Checkbutton(subframe2, text="Neutral",variable = self.checkBoxVar[0], onvalue = 1, offvalue = 0,bg=bg,command=self.onCheckBoxChange)
        checkbutton.pack(side=tk.TOP)
        checkbutton = tk.Checkbutton(subframe2, text="Replacement",variable = self.checkBoxVar[1], onvalue = 1, offvalue = 0,bg=bg)
        checkbutton.pack(side=tk.TOP)
        
    def onCheckBoxChange(self):
        if(self.checkBoxVar[0].get()==0):
            self.fieldsEntry[2].entry.configure(state=tk.DISABLED)
        else:
            self.fieldsEntry[2].entry.configure(state=tk.NORMAL)
        

    # Set the portrait
    def loadImageToPortrait(self,path):
        data="data.txt"
        length=-len(data)
        if(data in path.lower()):
            path=path[:length]+"portrait.png"
        else:
            path=""
        CommonFunctions.addImage(path,self.master.skillFields.portrait,72,True)          
            

    ## Open a existing file for edit it.
    def editFile(self):

        self.filename=CommonFunctions.askEditFile("Select a Hero file")
        if(self.filename==None):
            return None

        self.loadImageToPortrait(self.filename)

        for field in self.fieldsEntry:
            field.empty()

        self.checkBoxVar[0].set(0)
        self.fieldsEntry[2].entry.configure(state=tk.DISABLED)

        
        labels=self.master.skillFields.allSkills
        for i in range(0,len(labels)):
            labels[i].set("None")
            labels[i].configure(background="white")

        ## Made a backup of the opened file.
        CommonFunctions.madeBackUp("hero_backup.txt",self.filename)

        if(self.filename.endswith(" Replacement data.txt")):
            self.checkBoxVar[1].set(1)
        else:
            self.checkBoxVar[1].set(0)
           
        
        file1 = open(self.filename, 'r')
        self.lines=file1.readlines()
        self.count=0
        filled=[]
        
        while self.count<len(self.lines):
            line=self.lines[self.count].strip()
            
            ## If found Name, check the next line. If the next line do not exist because it
            ## check than this is illegal, continue without increment.
            if(line.startswith(fields[0]) and fields[0] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.fieldsEntry[0].set(answer)
                    filled+=[fields[0]]
                continue
            if(line.startswith(fields[1]) and fields[1] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.fieldsEntry[1].set(answer)
                    filled+=[fields[1]]
                continue
            if(line.startswith(fields[2]) and fields[2] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.fieldsEntry[2].set(answer)
                    filled+=[fields[2]]
                    self.checkBoxVar[0].set(1)
                    self.fieldsEntry[2].entry.configure(state=tk.NORMAL)
                continue

            ## If found Skills, read all lines after it and stop when found a blank.
            if(line.startswith(fields[3])):
                answer=self.getNextLine()
                lin=0
                listOfSkills=[]
                
                while(answer !=None):
                    labels[lin].set(answer)
                    if(answer in listOfSkills):
                        labels[lin].configure(background="red")
                    else:
                        listOfSkills+=[answer]
                    lin+=1
                    answer=self.getNextLine()
                else:
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
        
        labels=self.master.skillFields.allSkills
        listOfSkills=[]
        
        for label in labels:
            if(label.get() in listOfSkills):
                label.configure(background="red")
                return
            listOfSkills+=[label.get()]
            if(label.get() == "None"):
                break
        if(not self.filename.endswith(" Replacement data.txt") and self.checkBoxVar[1].get()==1):
            self.filename=self.filename[:-len("data.txt")]+"Replacement data.txt"
        if(self.filename.endswith(" Replacement data.txt") and self.checkBoxVar[1].get()==0):
            self.filename=self.filename[:-len("Replacement data.txt")]+"data.txt"


        self.filename=CommonFunctions.askSaveFile(self.filename,"Save Hero file")
        if(self.filename==None):
            self.filename=None
            return

        self.loadImageToPortrait(self.filename)
        
        file1 = open(self.filename, 'w')
        file1.write(fields[0]+"\n")
        file1.write(self.fieldsEntry[0].get().strip()+"\n\n")

        if(self.checkBoxVar[0].get() == 1 and len(self.fieldsEntry[2].get().strip())>0):
            file1.write(fields[2]+"\n")
            file1.write(self.fieldsEntry[2].get().strip()+"\n\n")

        file1.write(fields[1]+"\n")
        file1.write(self.fieldsEntry[1].get().strip()+"\n\n")

        file1.write(fields[3]+"\n")
        labels=self.master.skillFields.allSkills
        for label in labels:
            if(label.get() == "None"):
                break
            else:
                file1.write(label.get()+"\n")
        file1.close()

class TabHeroEditor(CommonClass.Tab):     
    def  __init__(self,master,window,**kwargs):
        CommonClass.Tab.__init__(self,master,window,**kwargs)

        self.pack(fill=tk.BOTH,expand=True)
        self.simpleFields=SimpleFields(self)
        self.skillFields=SkillFields(self)
        
    def onKeyRelease(self,event):
         # If the user is on an entry / input field, skip the event.
        if(CommonFunctions.checkIfInputField(type(self.focus_get()))):
            return  
        
        if(event.char=='d'):
            self.simpleFields.editFile()
        if(event.char=='v'):
            self.simpleFields.saveFile()
        

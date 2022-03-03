import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os
import ListSearchBar
from PIL import Image,ImageTk


fields=["Name","Unit","Class","Skills"]

## Contains the search bar, the description (placed wrongly) and the skill tree.
class SkillFields(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master,padx=5,pady=5)
        self.master=master
        self.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        subframe0=ttk.Frame(self,borderwidth=1,relief="sunken")
        subframe0.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))

        self.currentSlot=None
        self.allSkills=[]

        self.searchBar=ListSearchBar.SearchBar(subframe0,self)

        subframe1=ttk.LabelFrame(self.master.simpleFields,text='Description Skill', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,expand=True,side=tk.TOP,padx=(1,1),pady=(1,1))

        self.labelDesc=ttk.Label(subframe1,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.LEFT,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)
        self.labelDesc.configure(text=self.searchBar.descriptionsSkills["None"])

        frame=tk.Frame(self)
        frame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))
        subframe2=ttk.LabelFrame(frame,text='Skill Tree', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        subframe3=ttk.LabelFrame(frame,text='Informations', padding=(5, 5))
        subframe3.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1),expand=True)

        self.portrait = tk.Label(subframe3,text="NO PORTRAIT")
        self.portrait.pack()

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
            
    def createLabel(self,frame):
        v = tk.StringVar()
        
        label=LabelSimplified(frame,padding=(2,2),background="white",width=20,borderwidth=1,relief="sunken")
        label.set("None")
        label.pack(side=tk.LEFT,padx=1,pady=1)
        label.bind("<Button-1>",self.on_enter)
        self.allSkills+=[label]

    def on_enter(self,event):
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

                
## Label do not have set and get method. This class will do that.     
class LabelSimplified(tk.Entry):
    def __init__(self,master=None,**kwargs):
        self.var= tk.StringVar(master)
        ttk.Label.__init__(self,master,textvariable=self.var,**kwargs)
        self.get,self.set=self.var.get,self.var.set

## Contains edit, save and the three simple fields.
class SimpleFields(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master,padx=5,pady=5)
        self.master=master
        self.filename=None
        
        self.pack(side=tk.RIGHT,fill=tk.Y,expand=False)

        subframe1=ttk.LabelFrame(self,text='File', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        
        editButton=ttk.Button(subframe1,text='Edit (D)',command=self.editFile,width=12)
        editButton.pack(side=tk.LEFT,padx=5,pady=5)

        saveButton=ttk.Button(subframe1,text='Save as (V)',command=self.saveFile,width=12)
        saveButton.pack(side=tk.LEFT,padx=5,pady=5)

        subframe2=ttk.LabelFrame(self,text='Fields', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        subframe3=ttk.Frame(subframe2,borderwidth=1,relief="sunken")
        subframe3.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        label=ttk.Label(subframe3,text="Name:")
        label.pack(side=tk.LEFT,padx=5,pady=5)

        self.name_entry=tk.Entry(subframe3, font='bold',justify='center')
        self.name_entry.pack(fill=tk.X,padx=5,expand=True)
        self.name_entry.insert(0,"Hero name")

        subframe4=ttk.Frame(subframe2,borderwidth=1,relief="sunken")
        subframe4.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        label=ttk.Label(subframe4,text="Unit:")
        label.pack(side=tk.LEFT,padx=5,pady=5)

        self.unit_entry=tk.Entry(subframe4, font='bold',justify='center')
        self.unit_entry.pack(fill=tk.X,padx=5,expand=True)
        self.unit_entry.insert(0,"Starting Unit")

        subframe5=ttk.Frame(subframe2,borderwidth=1,relief="sunken")
        subframe5.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))

        label=ttk.Label(subframe5,text="Class:")
        label.pack(side=tk.LEFT,padx=5,pady=5)

        self.class_entry=tk.Entry(subframe5, font='bold',justify='center')
        self.class_entry.pack(fill=tk.X,padx=5,expand=True)
        self.class_entry.insert(0,"")


        
    ## Made a backup.
    def madeBackUp(self,filename):
        file1 = open(self.filename, 'r')
        lines=file1.readlines()

        backup = open("hero_backup.txt", 'w')
        backup.writelines(lines)
        
        file1.close()
        backup.close()

    def loadImageToPortrait(self,path):
        data="data.txt"
        length=-len("data.txt")
        if(data in path):
            path=path[:length]+"portrait.png"
        else:
            path=""
        if(os.path.exists(path)):
            image = self.addBlackOutline(path)
            n_image = image.resize((64, 64))
            photo = ImageTk.PhotoImage(n_image)
            self.master.skillFields.portrait.image = photo # <== this is were we anchor the img object
            self.master.skillFields.portrait.configure(image=photo)
            self.master.skillFields.portrait.pack(fill=tk.BOTH,side=tk.TOP)
        else:
            self.master.skillFields.portrait.image = None 
            self.master.skillFields.portrait.configure(image=None,text="NO PORTRAIT")
            self.master.skillFields.portrait.pack(fill=tk.BOTH,side=tk.TOP)            
            
    def addBlackOutline(self,path):
        image=Image.open(path)
        w=image.size[0]
        h=image.size[1]
        gameImage=Image.new("RGBA", (w, h), (0, 0, 0, 0)) 
        pixels = image.load()
        pixelsBlack=gameImage.load()

        for i in range(w):
            for j in range(h):
                if(pixels[i,j][3]!=0):
                    if(j+1<h):
                        pixelsBlack[i, j + 1] = (0, 0, 0, 255)
                    if(j-1>=0):
                        pixelsBlack[i, j - 1] = (0, 0, 0, 255)
                    if(i+1<w):
                        pixelsBlack[i + 1, j] = (0, 0, 0, 255)
                    if(i-1>=0):
                        pixelsBlack[i - 1, j] = (0, 0, 0, 255)
        for i in range(w):
            for j in range(h):
                if(pixels[i,j][3]!=0):
                    pixelsBlack[i, j] = pixels[i,j]
                       
        return gameImage


    ## Open a existing file for edit it.
    def editFile(self):

        
        self.filename=fd.askopenfilename(title="Select a hero file",filetypes=[("TXT Files","*.txt")])
        

        if(self.filename==None or self.filename.strip()==""):
            return None

        self.loadImageToPortrait(self.filename)
        
        self.name_entry.delete(0, tk.END)
        self.unit_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        labels=self.master.skillFields.allSkills
        for i in range(0,len(labels)):
            labels[i].set("None")
            labels[i].configure(background="white")

        ## Made a backup of the opened file.
        self.madeBackUp(self.filename)
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
                    self.name_entry.insert(0,answer)
                    filled+=[fields[0]]
                continue
            if(line.startswith(fields[1]) and fields[1] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.unit_entry.insert(0,answer)
                    filled+=[fields[1]]
                continue
            if(line.startswith(fields[2]) and fields[2] not in filled):
                answer=self.getNextLine()
                if(answer !=None):
                    self.class_entry.insert(0,answer)
                    filled+=[fields[2]]
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

        
        self.filename=fd.asksaveasfilename(initialfile=self.filename,title="Save Hero file",filetypes=[("TXT Files","*.txt")])
        if(len(self.filename.strip())==0):
            self.filename=None
            return
        if not self.filename.endswith(".txt"):
            self.filename+=".txt"

        self.loadImageToPortrait(self.filename)
        
        file1 = open(self.filename, 'w')
        file1.write("Name\n")
        file1.write(self.name_entry.get()+"\n\n")
        
        file1.write("Class\n")
        file1.write(self.class_entry.get()+"\n\n")

        file1.write("Unit\n")
        file1.write(self.unit_entry.get()+"\n\n")

        file1.write("Skills\n")
        labels=self.master.skillFields.allSkills
        for label in labels:
            if(label.get() == "None"):
                break
            else:
                file1.write(label.get()+"\n")
        file1.close()

class TabHeroEditor(ttk.Frame):     
    def  __init__(self,master,window):
        ttk.Frame.__init__(self,master)

        self.master=master
        self.window=window
        self.pack(fill=tk.BOTH,expand=True)
        self.simpleFields=SimpleFields(self)
        self.skillFields=SkillFields(self)
        
    def onKeyRelease(self,event):
         # If the user is on an entry / input field, skip the event.
        if(type(self.focus_get()) == tk.Entry or type(self.focus_get()) == ttk.Entry):
            return  
        
        if(event.char=='d'):
            self.simpleFields.editFile()
        if(event.char=='v'):
            self.simpleFields.saveFile()

    def bindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)
    def unBindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)
        

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os
import ListSearchBar


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

        subframe2=ttk.LabelFrame(self,text='Skill Tree', padding=(5, 5))
        subframe2.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))

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
        
        self.pack(side=tk.RIGHT,fill=tk.Y,expand=False)

        subframe1=ttk.LabelFrame(self,text='Config', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        
        editButton=ttk.Button(subframe1,text='Edit',command=self.editFile,width=12)
        editButton.pack(side=tk.LEFT,padx=5,pady=5)

        saveButton=ttk.Button(subframe1,text='Save as',command=self.saveFile,width=12)
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

        backup = open("backup.txt", 'w')
        backup.writelines(lines)
        

        file1.close()
        backup.close()


    ## Open a existing file for edit it.
    def editFile(self):
        self.filename=fd.askopenfilename(initialdir=os.getcwd(),title="Select a hero file",filetypes=[("TXT Files","*.txt")])
        

        if(self.filename==None or self.filename.strip()==""):
            return None
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
        while self.count<len(self.lines):
            line=self.lines[self.count].strip()

            ## If found Name, check the next line. If the next line do not exist because it
            ## check than this is illegal, continue without increment.
            if(line.startswith("Name")):
                answer=self.getNextLine()
                if(answer !=None and not self.checkIfIllegal(answer)):
                    self.name_entry.insert(0,answer)
                continue
            if(line.startswith("Unit")):
                answer=self.getNextLine()
                if(answer !=None and not self.checkIfIllegal(answer)):
                    self.unit_entry.insert(0,answer)
                continue
            if(line.startswith("Class")):
                answer=self.getNextLine()
                if(answer !=None and not self.checkIfIllegal(answer)):
                    self.class_entry.insert(0,answer)
                continue

            ## If found Skills, read all lines after it and stop when found a blank.
            if(line.startswith("Skills")):
                answer=self.getNextLine(True)
                lin=0
                listOfSkills=[]
                
                
                while(answer !=None):
                    labels[lin].set(answer)
                    if(answer in listOfSkills):
                        labels[lin].configure(background="red")
                    else:
                        listOfSkills+=[answer]
                    lin+=1
                    answer=self.getNextLine(True)
                else:
                    continue
            self.count+=1
        file1.close()
        
    ## Found the next line to read. Ignore blank line except if stopToBlank is True
    def getNextLine(self,stopToBlank=False):
        self.count+=1
        while self.count<len(self.lines):
            line=self.lines[self.count].strip()
            if(len(line)>0):
                return line
            else:
                return None

            self.count+=1
        return None

    ## Check if the text do not start with a illegal word.
    def checkIfIllegal(self,text):
        if(text.startswith("Skills")):
            return True
        if(text.startswith("Unit")):
            return True
        if(text.startswith("Name")):
            return True
        if(text.startswith("Class")):
            return True
        return False
    
            
    ## Save a file. Check if all field are valid.        
    def saveFile(self):

        if(self.checkIfIllegal(self.name_entry.get())):
            self.name_entry.configure(background="red")
            return
        if(self.checkIfIllegal(self.unit_entry.get())):
            self.unit_entry.configure(background="red")
            return            
        if(self.checkIfIllegal(self.class_entry.get())):
            self.unit_entry.configure(background="red")
            return                 
        
        labels=self.master.skillFields.allSkills
        listOfSkills=[]
        
        for label in labels:
            if(label.get() in listOfSkills):
                label.configure(background="red")
                return
            listOfSkills+=[label.get()]
            if(self.checkIfIllegal(label.get())):
                label.configure(background="red")
                return
            if(label.get() == "None"):
                break

        
        self.filename=fd.asksaveasfilename(initialdir=os.getcwd(),title="Save Hero file",filetypes=[("TXT Files","*.txt")])
        if not self.filename.endswith(".txt"):
            self.filename+=".txt"
        
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
        

## The application on the windows. Subdivided on two parts.
class Application(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master)

        self.master=master
        self.pack(fill=tk.BOTH,expand=True)
        self.simpleFields=SimpleFields(self)
        self.skillFields=SkillFields(self)

    def on_closing(self):
        self.master.destroy()

## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title('Hero Editor')
        self.geometry("1200x450+100+300")
        
        app=Application(self)
        self.protocol("WM_DELETE_WINDOW",app.on_closing)


if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()

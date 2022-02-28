import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os
import ListSearchBar


class LeftWindow(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master,padx=5,pady=5)
        self.master=master
        self.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        subframe0=ttk.Frame(self,borderwidth=1,relief="sunken")
        subframe0.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1))

        self.currentHover=None
        self.allSkills=[]

        self.searchBar=ListSearchBar.SearchBar(subframe0,self)

        subframe1=ttk.LabelFrame(self.master.rightWindow,text='Description Skill', padding=(5, 5))
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
        if(self.currentHover!=None):
            self.currentHover.configure(background="white")
        self.currentHover=event.widget
        self.labelDesc.configure(text=self.searchBar.descriptionsSkills[self.currentHover.get()])
        self.currentHover.configure(background="green")

    def setValue(self,value):
        self.currentHover.set(value)
##        self.currentHover.configure(text=value)
        labels=self.allSkills
        for label in labels:
            if(label==self.currentHover):
                return
            if(label.get() == "None"):
                label.configure(background="red")

                
        
class LabelSimplified(tk.Entry):
    def __init__(self,master=None,**kwargs):
        self.var= tk.StringVar(master)
        ttk.Label.__init__(self,master,textvariable=self.var,**kwargs)
        self.get,self.set=self.var.get,self.var.set

class RightWindow(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master,padx=5,pady=5)
        self.master=master
        
        self.pack(side=tk.RIGHT,fill=tk.Y,expand=False)

        subframe1=ttk.LabelFrame(self,text='Config', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1))
        
        # edit config button
        editconfigButton=ttk.Button(subframe1,text='Edit',command=self.editConfig,width=12)
        editconfigButton.pack(side=tk.LEFT,padx=5,pady=5)

        # save config button
        saveconfigButton=ttk.Button(subframe1,text='Save',command=self.saveConfig,width=12)
        saveconfigButton.pack(side=tk.LEFT,padx=5,pady=5)

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

    def madeBackUp(self,filename):
        file1 = open(self.filename, 'r')
        lines=file1.readlines()

        backup = open("backup.txt", 'w')
        backup.writelines(lines)
        

        file1.close()
        backup.close()


    def editConfig(self):
        self.filename=fd.askopenfilename(initialdir=os.getcwd(),title="Select a non-neutral hero file",filetypes=[("TXT Files","*.txt")])
        

        if(self.filename==None or self.filename.strip()==""):
            return None

        self.madeBackUp(self.filename)
        file1 = open(self.filename, 'r')
        self.lines=file1.readlines()
        self.count=0
        while self.count<len(self.lines):
            line=self.lines[self.count].strip()
            if(line.startswith("Name")):
                answer=self.getNextLine(False)
                if(answer !=None):
                    self.name_entry.delete(0, tk.END)
                    self.name_entry.insert(0,answer)
            if(line.startswith("Unit")):
                answer=self.getNextLine(False)
                if(answer !=None):
                    self.unit_entry.delete(0, tk.END)
                    self.unit_entry.insert(0,answer)
            if(line.startswith("Skills")):
                answer=self.getNextLine(True)
                lin=0
                listOfSkills=[]
                
                labels=self.master.leftWindow.allSkills
                while(answer !=None):
                    labels[lin].set(answer)
                    if(answer in listOfSkills):
                        labels[lin].configure(background="red")
                    else:
                        listOfSkills+=[answer]
                    lin+=1
                    answer=self.getNextLine(True)
                else:
                    for i in range(lin,len(labels)):
                        labels.configure(background="red")
                    continue

                

            self.count+=1
        file1.close()
    def getNextLine(self,stopToBlank):
        self.count+=1
        while self.count<len(self.lines):
            line=self.lines[self.count].strip()
            if(len(line)>0):
                return line
            else:
                return None

            self.count+=1
        return None

    def checkIfIllegal(self,widget):
        if(widget.get().startswith("Skills")):
            return True
        if(widget.get().startswith("Unit")):
            return True
        if(widget.get().startswith("Name")):
            return True
        return False
            
                
    def saveConfig(self):

        if(self.checkIfIllegal(self.name_entry.get())):
            self.name_entry.configure(background="red")
            return
        if(self.checkIfIllegal(self.unit_entry.get())):
            self.unit_entry.configure(background="red")
            return            
        
        
        labels=self.master.leftWindow.allSkills
        listOfSkills=[]
        
        for label in labels:
            if(label.get() in listOfSkills):
                label.configure(background="red")
                return
            listOfSkills+=[label.get()]
            if(self.checkIfIllegal(label)):
                label.configure(background="red")
                return
            if(label.get() == "None"):
                break

        
        self.filename=fd.asksaveasfilename(initialdir=os.getcwd(),title="Save non-neutral Hero file",filetypes=[("TXT Files","*.txt")])
        if not self.filename.endswith(".txt"):
            self.filename+=".txt"
        
        
        file1 = open(self.filename, 'w')
        file1.write("Name\n")
        file1.write(self.name_entry.get()+"\n\n")
        file1.write("Unit\n")
        file1.write(self.unit_entry.get()+"\n\n")
        file1.write("Skills\n")
        labels=self.master.leftWindow.allSkills
        for label in labels:
            if(label.get() == "None"):
                break
            else:
                file1.write(label.get()+"\n")
        file1.close()
        

class Application(tk.Frame):
    def  __init__(self,master):
        tk.Frame.__init__(self,master)

        self.master=master
        self.pack(fill=tk.BOTH,expand=True)
        self.rightWindow=RightWindow(self)
        self.leftWindow=LeftWindow(self)

    def on_closing(self):
        self.master.destroy()

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

import tkinter as tk
import tkinter.ttk as ttk

## Label do not have set and get method. This class will do that.     
class LabelSimplified(tk.Entry):
    def __init__(self,master=None,**kwargs):
        self.var= tk.StringVar(master)
        ttk.Label.__init__(self,master,textvariable=self.var,**kwargs)
        self.get,self.set=self.var.get,self.var.set

class FileFrame(ttk.LabelFrame):
    def __init__(self,master=None,side=tk.TOP,**kwargs):
        ttk.LabelFrame.__init__(self,master,text='File', padding=(5, 5))
        self.master=master
        self.pack(fill=tk.BOTH,side=side,padx=(1,1),pady=(1,1))
                
        editButton=ttk.Button(self,text='Edit (D)',command=self.master.editFile,width=12)
        editButton.pack(side=tk.LEFT,padx=5,pady=5)

        saveButton=ttk.Button(self,text='Save as (V)',command=self.master.saveFile,width=12)
        saveButton.pack(side=tk.LEFT,padx=5,pady=5)

class Field(tk.Frame):
    def __init__(self,master,titleField,hintField="",side=tk.TOP,**kwargs):
        tk.Frame.__init__(self,master,borderwidth=1,relief="sunken")
        self.pack(fill=tk.BOTH,side=side,padx=(1,1),pady=(1,1))
                
        label=ttk.Label(self,text=titleField)
        label.pack(side=tk.LEFT,padx=5,pady=5)

        self.entry=tk.Entry(self, font='bold',justify='center')
        self.entry.pack(fill=tk.X,padx=5,expand=True)
        if(hintField!=None):
            self.set(hintField)
    def get(self):
        return self.entry.get()
    def set(self,text):
        self.entry.insert(0,text)
    def empty(self):
        self.entry.delete(0, tk.END)

class Tab(ttk.Frame):
    def  __init__(self,master,window):
        ttk.Frame.__init__(self,master)
        self.master=master
        self.window=window
    
    def onKeyRelease(self,event):
        None
    def bindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)
    def unBindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)    


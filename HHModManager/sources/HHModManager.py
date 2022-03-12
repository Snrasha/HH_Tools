import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os, zipfile


def askZipFile():
    filename=fd.askopenfilename(title="Select a mod to install",filetypes=[("ZIP Files","*.zip")])
    if(filename==None or filename.strip()==""):
        filename=None
    return filename
def askPathDir():
    filename=fd.askdirectory(title="Select the path where install mod")
    if(filename==None or filename.strip()==""):
        filename=None
    return filename

def savePrefs(path):
    file = open("prefs.data", 'w')
    file.write("path_game="+path+'\n')
    file.close()
def loadPrefs():

    params=[]
    if(os.path.exists("prefs.data")):
        file = open("prefs.data", 'r')
        lines=file.readlines()
        for line in lines:
            if(line.startswith("path_game")):
                params+=[line[len("path_game="):]]
        file.close()
    return params
    


    



class Field(ttk.Frame):
    def __init__(self,master,titleField,side=tk.TOP,sideLabel=tk.LEFT,**kwargs):
        ttk.Frame.__init__(self,master)
        self.pack(fill=tk.BOTH,side=side,padx=(1,1),pady=(1,1))
        self.titleField=titleField
        label=ttk.Label(self,text=titleField)
        self.entry=tk.Entry(self, font='bold')
        self.entry.pack(side=tk.RIGHT,fill=tk.X,padx=5,expand=True)
        label.pack(side=sideLabel,padx=5,pady=5)

    def get(self):
        return self.entry.get()
    def set(self,text):
        self.empty()
        if(text==None):
            return
        self.entry.insert(0,text)
    def empty(self):
        self.entry.delete(0, tk.END)
class ZipField(Field):
    def __init__(self,master,titleField,side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField)
        self.entry.bind("<Button-1>",self.onEnter)
    def onEnter(self,event):
        filename=askZipFile()
        if(filename!=None):
            self.set(filename)
        self.master.focus()
class PathField(Field):
    def __init__(self,master,titleField,side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField)
        self.entry.bind("<Button-1>",self.onEnter)
    def onEnter(self,event):
        filename=askPathDir()
        if(filename!=None):
            self.set(filename)
        self.master.focus()

        

def checkIfInputField(compare):
    return (compare == tk.Text or\
           compare == tk.Entry or\
           compare == ttk.Entry)

class Application(ttk.Frame):
    def  __init__(self,window):
        ttk.Frame.__init__(self,window)

        style = ttk.Style(window)
        style.theme_use('clam')

        self.window=window
        self.pack(fill=tk.BOTH,expand=True)
        self.bg = style.lookup('TFrame', 'background')

        self.params=loadPrefs()


        self.window.bind("<KeyPress>", self.onKeyDown)
        self.window.bind('<Escape>', self.onEscape)

        frame1=ttk.Frame(self,borderwidth=1,relief="sunken",padding=(5,5))
        frame1.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        
        frame2=ttk.Frame(self,borderwidth=1,relief="sunken",padding=(5,5))
        frame2.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        
        self.zipField=ZipField(frame1,"Mod to install")
        self.zipField.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        button=ttk.Button(frame1,text="Install")
        button.pack(fill=tk.BOTH,side=tk.RIGHT)

        self.folderModField=PathField(frame2,"Hero's hour Path")
        self.folderModField.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        self.folderModField.set(self.params)
        

        self.checkBoxVar=[]
        self.checkBoxVar+=[tk.IntVar()]
        self.enablemod_checkbtn = tk.Checkbutton(frame2,text="Enable mods", variable = self.checkBoxVar[0], onvalue = 1, offvalue = 0,bg=self.bg,command=self.onCheckBoxChange)
        self.enablemod_checkbtn.pack(side=tk.RIGHT)

        frame3=ttk.Frame(self,borderwidth=1,relief="sunken",padding=(5,5))
        frame3.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))

        

    def onCheckBoxChange(self):
        None
    def onClosing(self):
        savePrefs(self.folderModField.get())
        self.window.destroy()
        
        

    def onEscape(self,event):
        # Exit the input field or any Entry
        self.window.focus()
    

    # Switch the tab and disable key listener of the old tab and enable for the new tab.
    def onKeyDown(self,event):
        if(len(event.char)!=1):
            return
        # If the user is on an entry / input field, skip the event.
        if(checkIfInputField(type(self.focus_get()))):
            # When press Enter, remove the focus if Entry.
            if(ord(event.char)==13):
                self.window.focus()
            return

## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title("Hero's hour Mod Manager")
        self.geometry("700x350+100+300")
        
        app=Application(self)
        self.protocol("WM_DELETE_WINDOW", app.onClosing)
        
if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os, zipfile,shutil
import MODSETTINGS

def containsTypicalFolder(li):
    for i in li:
        if i == "Artifacts":
            return True
        if i == "Factions":
            return True        
        if i == "Hero classes":
            return True
        if i == "Hero replacements":
            return True
        if i == "Neutral heroes":
            return True
        if i == "Neutral units":
            return True
        if i == "Projectiles":
            return True
        if i == "Unit replacements":
            return True 
def copyModdingSettings(path):
    modsettings = open(path, 'r')
    lines=modsettings.readlines()
    modsettings.close()
    modsettings = open("MODSETTINGS.py", 'w')
    modsettings.write("txt="+str(lines)+'\n')
    modsettings.close()
def createModSettings(path):
    modsettings = open(path, 'w')
    for l in MODSETTINGS.txt:
        modsettings.write(l)
    modsettings.close()
def writeModsInSettings(path,mods,informations):
    modsettings = open(path, 'w')
    modsettings.write(MODSETTINGS.txt[0])
    for l in mods:
        modsettings.write(l+"\n")
    modsettings.write("\n")
    for l in informations:
        modsettings.write(l)
    modsettings.close()
def getAllDir(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    
def getModsEnabledInSettings(path):
    modsettings = open(path, 'r')
    lines=modsettings.readlines()
    mods=[]
    informations=["\n"]
    inc=1
    length=len(lines)
    if(length>2):
        if(lines[0].startswith("LOAD MODS")):
            while inc < length:
                l=lines[inc].strip()
                if(l.startswith("--------------------------")):
                    break
                mods+=[l]
                inc+=1
    while inc < length:
        informations+=[lines[inc]]
        inc+=1
                



    return (mods,informations)
            
        
    
    

def askZipFile():
    filename=fd.askopenfilename(title="Select a mod to install",filetypes=[("ZIP Files","*.zip")])
    if(filename==None or filename.strip()==""):
        filename=None
    return filename
def askPathDir(txt):
    filename=fd.askdirectory(title=txt)
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
                params+=[line[len("path_game="):].strip()]
        file.close()
    return params

def readIfModEnable(path):
    file = open(path, 'r')
    lines=file.readlines()
    file.close()
    return int(lines[20].strip())
    
def enableMod(path,enable):
    file = open(path, 'r')
    lines=file.readlines()
    file.close()
    lines[20]=str(enable)
    
    file = open(path, 'w')
    for l in lines:
        file.write(l.strip()+'\n')
    file.close()    
    
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
        self.mods=[]
        self.informations=[]
        self.correctPath=False
    def onEnter(self,event):
        filename=askPathDir("Select the path where install mod")
        self.setPath(filename)
    def getMods(self):
        if(self.correctPath):
            return self.modsPresent
        else:
            return None
    def setPath(self,filename):
        self.set(filename)
        if(filename!=None):
            self.set(filename)
        # Check if correct folder
        if(os.path.exists(filename+"/Hero's Hour.exe")):
            self.entry.configure(background="green")
            directory=filename
            directory+="/mods"
            if(os.path.exists(directory)):
                None
            else:
                os.mkdir(directory)
            if not(os.path.exists(directory+"/MOD SETTINGS.txt")):
                createModSettings(directory+"/MOD SETTINGS.txt")
            self.modsEnabled,self.informations=getModsEnabledInSettings(directory+"/MOD SETTINGS.txt")
            self.modsPresent=getAllDir(directory)
            print(self.modsPresent)
            self.correctPath=True
            
        else:
            self.entry.configure(background="red")
            self.correctPath=False
        
        self.master.focus()
class LocalPathField(Field):
    def __init__(self,master,titleField,side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField)
        self.entry.bind("<Button-1>",self.onEnter)
        filename=os.getenv('LOCALAPPDATA')+"/Hero_s_Hour"
        filename=filename.replace("\\","/")
        self.set(filename)
        if(os.path.exists(filename)):
            if(os.path.exists(filename+"/opt.txt")):
                self.entry.configure(background="green")
            else:
                self.entry.configure(background="red")
        else:
            self.entry.configure(background="red")

        
    def onEnter(self,event):
        filename=askPathDir("Select the AppData/Local/Game")
        if(os.path.exists(filename+"/opt.txt")):
            self.entry.configure(background="green")
        else:
            self.entry.configure(background="red")
        self.master.focus()

class ModsField(ttk.Frame):
    def __init__(self,master,**kwargs):
        ttk.Frame.__init__(self,master)
        

        frame1=ttk.Frame(self)
        frame1.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3),expand=True)
        frame2=ttk.Frame(self)
        frame2.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3),expand=True)
               
        label=ttk.Label(frame1,text="Mods disabled")
        label.pack(side=tk.TOP,padx=5,pady=5)
        self.listbox1 = tk.Listbox(frame1)
        self.listbox1.pack(side=tk.TOP,padx=5,pady=5)
        
        label=ttk.Label(frame2,text="Mods enabled")
        label.pack(side=tk.TOP,padx=5,pady=5)
        self.listbox1 = tk.Listbox(frame2)
        self.listbox1.pack(side=tk.TOP,padx=5,pady=5)
##        self.listbox1.bind('<Double-Button-1>', self.onDoubleClickList1)
##        self.listbox1.bind('<<ListboxSelect>>', self.onSelectListBox)

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
        subframe1=ttk.Frame(frame1)
        subframe1.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        subframe2=ttk.Frame(frame1)
        subframe2.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        subframe3=ttk.Frame(frame1)
        subframe3.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        

        self.zipField=ZipField(subframe1,"Mod to install")
        self.zipField.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        button=ttk.Button(subframe1,text="Install",command=self.onInstall)
        button.pack(fill=tk.BOTH,side=tk.RIGHT)

        self.folderModField=PathField(subframe2,"Hero's hour Path")
        self.folderModField.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        self.folderModField.setPath(self.params[0])
        self.localField=LocalPathField(subframe3,"Local Path")
        self.localField.pack(fill=tk.BOTH,side=tk.BOTTOM,expand=True)

        

        
              
    
        self.checkBoxVar=tk.IntVar()
        self.enablemod_checkbtn = tk.Checkbutton(subframe2,text="Enable mods", variable = self.checkBoxVar, onvalue = 1, offvalue = 0,bg=self.bg,command=self.onCheckBoxChange)
        self.enablemod_checkbtn.pack(side=tk.RIGHT)

        

        frame2=ttk.Frame(self,borderwidth=1)
        frame2.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
        
        frame3=ttk.Frame(frame2,borderwidth=1,relief="sunken",padding=(5,5))
        frame3.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3),expand=True)
        frame4=ttk.Frame(frame2,borderwidth=1,relief="sunken",padding=(5,5))
        frame4.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(3,3),pady=(3,3),expand=True)
        
        label=ttk.Label(frame4,text="Mods from Steam are not visible here. Do not install duplicate.")
        label.pack(side=tk.TOP,padx=5,pady=5)
        
        mf=ModsField(frame3)
        mf.pack(fill=tk.BOTH,side=tk.LEFT)

        v=readIfModEnable(self.localField.get()+"/opt.txt")
        self.checkBoxVar.set(v)

        
    def onCheckBoxChange(self):
        enableMod(self.localField.get()+"/opt.txt",self.checkBoxVar.get())

    def onClosing(self):
        savePrefs(self.folderModField.get())
        self.window.destroy()

    def onInstall(self):
        zifile=self.zipField.get()
        directory=self.folderModField.get()
        mods=self.folderModField.getMods()
        if(mods==None):
            return
        else:
            
            if(zipfile.is_zipfile(zifile)):
                namemod=zifile.split("/")
                namemod=namemod[-1].split('.')
                b=namemod[0]
                for i in range(1,len(namemod)-1):
                    b="."+namemod[i]
                namemod=b
                tmp="tmp"
                inc=0
                while(os.path.exists(tmp+str(inc))):
                    inc+=1
                os.mkdir(tmp+str(inc))
                with zipfile.ZipFile(zifile, 'r') as zip_ref:
                    zip_ref.extractall(tmp+str(inc))
                self.copyTmpToMods(tmp+str(inc),namemod,directory)
                shutil.rmtree(tmp+str(inc)) 

    def getParentAndFiles(self,tmp,parent):
        files=getAllDir(tmp)
        if(containsTypicalFolder(files)):
            return (tmp,parent)
        else:
            for i in files:
                f=self.getParentAndFiles(tmp+"/"+i,i)
                if(f!=None):
                    return f
            return None
        
        

    def copyTmpToMods(self,tmp,namemod,directory):
        
        target_dir = directory+"/mods/"
        source_dir,addTarget=self.getParentAndFiles(tmp,None)
        print(source_dir)

        files=getAllDir(source_dir)
        if(addTarget!=None):
            target_dir+=addTarget
        else:
            target_dir+=namemod
        print(target_dir)
        print(files)
        if(os.path.exists(target_dir)):
            shutil.rmtree(target_dir)
        os.mkdir(target_dir)
        for fil in files:
            shutil.move(os.path.join(source_dir, fil), target_dir)        

        
##        if(len(files)==1):
##            print(files)
##            for fil in files:
##                shutil.move(os.path.join(source_dir, fil), target_dir)
##        else:
##            if(os.path.exists(directory+"/mods/"+namemod)):
##               shutil.rmtree(directory+"/mods/"+namemod) 
##            os.mkdir(directory+"/mods/"+namemod)
##            target_dir+=namemod
##            print(files)
##            for fil in files:
##                shutil.move(os.path.join(source_dir, fil), target_dir)
                   
        

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



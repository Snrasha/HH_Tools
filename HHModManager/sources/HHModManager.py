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
    informations=[]
    inc=1
    length=len(lines)
    if(length>2):
        if(lines[0].startswith("LOAD MODS")):
            while inc < length:
                l=lines[inc].strip()
                if(l.startswith("--------------------------")):
                    break
                if(len(l)==0):
                    inc+=1
                    continue
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
def askPathDir(txt,initialdir=None):
    filename=fd.askdirectory(initialdir=initialdir,title=txt)
    if(filename==None or filename.strip()==""):
        filename=None
    return filename
def savePrefs(path,localpath):
    file = open("prefs.data", 'w')
    file.write("path_game="+path+'\n')
    if(localpath!=None):
        file.write("local_path_game="+localpath+'\n')
    file.close()
def loadPrefs():

    params=[None,None]
    if(os.path.exists("prefs.data")):
        file = open("prefs.data", 'r')
        lines=file.readlines()
        for line in lines:
            if(line.startswith("path_game")):
                params[0]=line[len("path_game="):].strip()
            if(line.startswith("local_path_game")):
                params[1]=line[len("local_path_game="):].strip()
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
    if(len(lines)<21):
        return False
    lines[20]=str(enable)
    
    file = open(path, 'w')
    for l in lines:
        file.write(l.strip()+'\n')
    file.close()
    return True

    
    
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
    def __init__(self,master,titleField,modlist,side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField)
        self.entry.bind("<Button-1>",self.onEnter)
        self.mf=modlist
        self.informations=[]
        self.modsPresent=None
        self.modsEnabled=None
    def onEnter(self,event):
        filename=askPathDir("Select the path where install mod")
        self.setPath(filename)

    def setPath(self,filename):
        if(filename==None):
            return
        # Check if correct folder
        if(filename!=None and os.path.exists(filename+"/Hero's Hour.exe")):
            self.set(filename)
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
            self.mf.update(self.modsPresent,self.modsEnabled)
        else:
            self.entry.configure(background="red")
            self.modsPresent=None
            self.modsEnabled=None

        self.master.focus()
    def updateModsPresent(self):
        self.modsPresent=getAllDir(self.get()+"/mods")
    def save(self):
        
        if(self.modsEnabled!=None and self.informations!=None):
            writeModsInSettings(self.get()+"/mods/MOD SETTINGS.txt",self.modsEnabled,self.informations)
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
        self.customPath=None

        
    def onEnter(self,event):
        filename=askPathDir("Select the AppData/Local/Game",os.getenv('LOCALAPPDATA'))
        
        if(filename!=None and os.path.exists(filename+"/opt.txt")):
            self.entry.configure(background="green")
            self.customPath=filename
            self.set(filename)
        else:
            self.entry.configure(background="red")
        self.master.focus()

    def getCustom(self):
        return self.customPath
    def setCustom(self,customPath):
        if(customPath==None):
            return
        if(os.path.exists(customPath+"/opt.txt")):
            self.entry.configure(background="green")
            self.customPath=customPath
            self.set(customPath)
        else:
            self.entry.configure(background="red")

class ModsField(ttk.Frame):
    def __init__(self,master,folderField,**kwargs):
        ttk.Frame.__init__(self,master)
        self.folderField=folderField
        

        frame1=ttk.Frame(self)
        frame1.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3),expand=True)

        frame3=ttk.Frame(self)
        frame3.pack(fill=tk.BOTH,side=tk.BOTTOM,padx=(3,3),pady=(3,3),expand=True)
        frame2=ttk.Frame(self)
        frame2.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3),expand=True)     
        label=ttk.Label(frame1,text="Mods disabled")
        label.pack(side=tk.TOP,padx=5,pady=5)
        self.listbox1 = tk.Listbox(frame1)
        self.listbox1.pack(side=tk.TOP,padx=5,pady=5)
        
        label=ttk.Label(frame2,text="Mods enabled")
        label.pack(side=tk.TOP,padx=5,pady=5)
        self.listbox2 = tk.Listbox(frame2)
        self.listbox2.pack(fill=tk.BOTH,side=tk.TOP,padx=5,pady=5,expand=True)
        button=ttk.Button(frame3,text="Save",command=self.onClick)
        button.pack(fill=tk.BOTH,side=tk.TOP,padx=5,pady=5)

        self.listbox1.bind('<Double-Button-1>', self.onDoubleClickList1)
        self.listbox2.bind('<Double-Button-1>', self.onDoubleClickList2)

    def onDoubleClickList1(self,event):
        w = event.widget
        if(len(w.curselection())==0):
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        if not(value in self.folderField.modsEnabled):
            self.listbox2.insert(tk.END, value)
            self.folderField.modsEnabled+=[value]
    def onDoubleClickList2(self,event):
        w = event.widget
        if(len(w.curselection())==0):
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        if(value in self.folderField.modsEnabled):
            self.folderField.modsEnabled.remove(value)
        self.listbox2.delete(0, tk.END)
        for item in self.folderField.modsEnabled:
            self.listbox2.insert(tk.END, item)
    def onClick(self):
        self.folderField.save()
        
    def update(self,mods,modsEnabled):
        
        self.listbox1.delete( 0, tk.END)
        if(mods!=None):
            for item in mods:
                self.listbox1.insert( tk.END, item)
        self.listbox2.delete( 0, tk.END)
        if(modsEnabled!=None):
            for item in modsEnabled:    
                self.listbox2.insert( tk.END, item)       
        

def checkIfInputField(compare):
    return (compare == tk.Text or\
           compare == tk.Entry or\
           compare == ttk.Entry)

description="Do not install mods you already installed via the Steam Workshop."\
            "\n\nMods from Steam will not appear here."\
            "\n\nHH Steam Path: Program Files/Steam/steamapps/common/Hero's Hour."\
            
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

        self.folderModField=PathField(subframe2,"Hero's Hour Path",None)
        self.folderModField.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
        
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
        
        label=ttk.Label(frame4,text=description,wraplength=300)
        label.pack(fill=tk.BOTH,side=tk.TOP,padx=5,pady=5)
        
        self.mf=ModsField(frame3,self.folderModField)
        self.mf.pack(fill=tk.BOTH,side=tk.LEFT)

        self.folderModField.mf=self.mf
        self.folderModField.setPath(self.params[0])
        self.localField.setCustom(self.params[1])

        v=readIfModEnable(self.localField.get()+"/opt.txt")
        self.checkBoxVar.set(v)

##        self.mf.update(self.folderModField.modsPresent,self.folderModField.modsEnabled)

        
    def onCheckBoxChange(self):
        opt=self.localField.get()+"/opt.txt"
        success=False
        if(os.path.exists(opt)):
            success=enableMod(self.localField.get()+"/opt.txt",self.checkBoxVar.get())
        
        if not(boolean):
            if(self.checkBoxVar.get()==1):
                self.checkBoxVar.set(0)
            else:
                self.checkBoxVar.set(1)
           

    def onClosing(self):
        savePrefs(self.folderModField.get(),self.localField.getCustom())
        self.window.destroy()

    def onInstall(self):
        
        zifile=self.zipField.get().strip()
        directory=self.folderModField.get()
        mods=self.folderModField.modsPresent
        
        if(mods==None or len(zifile)==0):
            return
        else:
            
            if(zipfile.is_zipfile(zifile)):
                namemod=zifile.split("/")
                namemod=namemod[-1].split('.')
                b=namemod[0]
                for i in range(1,len(namemod)-1):
                    b+="."+namemod[i]
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

        
        self.folderModField.updateModsPresent()
        self.mf.update(self.folderModField.modsPresent,self.folderModField.modsEnabled)

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
##        print(source_dir)

        files=getAllDir(source_dir)
        if(addTarget!=None):
            target_dir+=addTarget
        else:
            target_dir+=namemod
##        print(target_dir)
##        print(files)
        if(os.path.exists(target_dir)):
            shutil.rmtree(target_dir)
        os.mkdir(target_dir)
        for fil in files:
            shutil.move(os.path.join(source_dir, fil), target_dir)        


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
        self.title("Hero's Hour Mod Manager")
        self.geometry("700x350+100+300")
        
        app=Application(self)
        self.protocol("WM_DELETE_WINDOW", app.onClosing)
        
if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()



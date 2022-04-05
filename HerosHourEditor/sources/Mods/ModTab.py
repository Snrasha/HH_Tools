import tkinter as tk
import tkinter.ttk as ttk
import Utils.CommonClass as CommonClass
import Utils.CommonFunctions as CommonFunctions
from tkinter import filedialog as fd
import os

spellTier=["Minor","Major","Ultimate","Adventure"]

class ModLoad(CommonClass.Tab):     
    def  __init__(self,master,window,**kwargs):
        CommonClass.Tab.__init__(self,master,window,**kwargs)
        self.pack(fill=tk.BOTH,expand=True)
        self.master=master
        style = ttk.Style(self)
        self.bg = style.lookup('TFrame', 'background')
        self.filename=None
        self.modsPath=[]
        self.leftFrameLayout()
        self.rightFrameLayout()
        self.currentTab=chr(49)
        self.loadPrefs()
        
        
    def leftFrameLayout(self):
        frame=ttk.LabelFrame(self,text='Custom Abilities, Skill and Spell found', padding=(5, 5))
        frame.pack(fill=tk.BOTH,side=tk.LEFT,padx=(1,1),pady=(1,1),expand=True)

        self.canvas=tk.Canvas(frame,bg=self.bg,relief=tk.FLAT,bd=0,highlightthickness=0)
        self.scrollbar1 = ttk.Scrollbar(frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar1.pack(fill=tk.Y,side=tk.RIGHT)
        self.canvas.pack(fill=tk.BOTH,side=tk.RIGHT,expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar1.set)

        self.leftFrame=ttk.Frame(self.canvas)
        self.leftFrame.pack(fill=tk.BOTH,expand=True)

    def reloadList(self):
        self.listbox.delete(0, tk.END)
        for widget in self.leftFrame.winfo_children():
            widget.destroy()
        
        for item in self.modsPath:
            
            try:
                nameMod=item[item.rindex("/")+1:]
                self.listbox.insert( tk.END,nameMod)
            except:
                nameMod="Error"
                None
            try:
                abilities,skills,spells=self.foundAllSkillsSpellsAbilities(item)
                maxi=max(len(abilities),len(skills),len(spells))
                
                frame=tk.Frame(self.leftFrame,bg=self.bg)
                frame.pack(side=tk.TOP)
                la=ttk.Label(frame,text=nameMod)
                la.pack(side=tk.TOP)                
                self.fillList(frame,"Abilities",abilities,maxi)
                self.fillList(frame,"Skills",skills,maxi)
                self.fillList(frame,"Spells",spells,maxi)
            except:
                None        
        
        self.leftFrame.update_idletasks()
        self.canvas.create_window((0, 0), window=self.leftFrame, anchor='w')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.set_mousewheel(self.canvas)
        self.set_mousewheel(self.scrollbar1)

    def fillList(self,frame,name,diction,maxi):
        subframe=ttk.LabelFrame(frame,text=name, padding=(5, 5))
        subframe.pack(side=tk.LEFT,padx=(1,1),pady=(1,1))
        listb = tk.Listbox(subframe)
        listb.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.set_disablemousewheel(listb)
        count=0
        for key in diction:
            listb.insert( tk.END,key)
            count+=1
        for i in range(maxi-count):
            listb.insert( tk.END,"")
        listb.config(height=0)
    def foundAllSkillsSpellsAbilities(self,path):
        skills={}
        abilities={}
        spells={}
        if not (os.path.exists(path)):
            return (abilities,skills,spells)
        folderpath=path+"/Custom Abilities"
        cusAbiList=self.getAllTextFiles(folderpath)
        folderpath=path+"/Custom Spells"
        cusSpellList=self.getAllTextFiles(folderpath)
        folderpath=path+"/Custom Skills"
        cusSkillList=self.getAllTextFiles(folderpath)

        for filename in cusAbiList:
            try:
                file = open(filename, 'r')
                lines=file.readlines()
                file.close()
                if(len(lines) >3):
                    key=lines[1].strip()
                    value=lines[4].strip()
                    abilities[key]=value
                    CommonFunctions.readAbilities()[key]=value
            except:
                None
        for filename in cusSkillList:
            try:
                file = open(filename, 'r')
                lines=file.readlines()
                file.close()
                if(len(lines) >7):
                    key=lines[4].strip()
                    value=lines[7].strip()
                    skills[key]=value
                    CommonFunctions.readSkills()[key]=value
            except:
                None
        for filename in cusSpellList:
            try:
                file = open(filename, 'r')
                lines=file.readlines()
                file.close()
                if(len(lines) >26):
                    tier=int(lines[7].strip())
                    key=lines[25].strip()
                    value=lines[19].strip()+"\nElemental School: "+lines[10].strip()+"\nTier: "+spellTier[tier]
                    spells[key]=value
                    if(tier <4):
                        CommonFunctions.readSpells()[key]=value
            except:
                None
        return (abilities,skills,spells)

            
        
    def getAllTextFiles(self,folderpath):
        if (os.path.exists(folderpath)):
            l=[os.path.join(folderpath, f) for f in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, f)) and f.endswith(".txt")]
        else:
            l=[]
        return l
    def set_mousewheel(self,widget):
        """Activate / deactivate mousewheel scrolling when
        cursor is over / not over the widget respectively."""
        widget.bind("<Enter>", lambda _: widget.bind_all('<MouseWheel>', self.onMouseWheel))
        widget.bind("<Leave>", lambda _: widget.unbind_all('<MouseWheel>'))
    def set_disablemousewheel(self,widget):
        widget.bind("<Enter>", lambda _: self.canvas.unbind_all('<MouseWheel>'))
        widget.bind("<Leave>", lambda _: self.canvas.bind_all('<MouseWheel>', self.onMouseWheel))        
        
    

    def onMouseWheel(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def rightFrameLayout(self):
        rightFrame=ttk.Frame(self)
        rightFrame.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(1,1),pady=(1,1),anchor="n")
        
        frame1=ttk.LabelFrame(rightFrame,text='Mod', padding=(5, 5))
        frame1.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1),expand=True)
        
        editButton=ttk.Button(frame1,text='Load Mod (D)',command=self.loadMod,width=12)
        editButton.pack(side=tk.TOP,padx=5,pady=5)
        label=CommonClass.LabelSimplified(frame1,justify=tk.CENTER)
        label.pack(fill=tk.BOTH,side=tk.TOP)
        label.configure(wraplength=200)
        label.set("After load a new mod, need a reload.")
        
        belowFrame=ttk.LabelFrame(rightFrame,text='List', padding=(5, 5))
        belowFrame.pack(fill=tk.BOTH,side=tk.TOP,padx=(1,1),pady=(1,1),expand=True)
        label=CommonClass.LabelSimplified(belowFrame,justify=tk.CENTER)
        label.pack(fill=tk.BOTH,side=tk.TOP)
        label.configure(wraplength=200)
        label.set("Double clic, for remove mod. Need a reload.")

        self.listbox = tk.Listbox(belowFrame)
        self.listbox.bind('<Double-Button-1>', self.onDoubleClickListBox)
        self.listbox.pack(side=tk.TOP,fill=tk.BOTH,padx=5,expand=True)

    def loadPrefs(self):
        if(os.path.exists("prefsHHEditor.data")):
            file = open("prefsHHEditor.data", 'r')
            lines=file.readlines()
            count=0
            while count < len(lines):
                line=lines[count].strip()
                count+=1
                if(len(line)==0):
                    continue
                if(line.startswith("[MODS]")):
                    while count < len(lines):
                        line=lines[count].strip()
                        count+=1
                        if(len(line)==0):
                            continue
                        
                        if(line.startswith("[")):
                            break
                        else:
                            self.modsPath+=[line.strip()]

                if(line.startswith("[SETUP]")):
                    line=lines[count].strip()
                    self.currentTab=line[0]
            file.close()
            self.reloadList()
        
        
    def savePrefs(self,currentTab=1):
        file = open("prefsHHEditor.data", 'w')
        file.write("[MODS]\n")
        for path in self.modsPath:
            file.write(path+'\n')
        file.write("[SETUP]\n")
        file.write(str(currentTab)+"\n")
        file.close()
    def askPathDir(self,txt):
        filename=fd.askdirectory(title=txt)
        if(filename==None or filename.strip()==""):
            filename=None
        return filename        
    def loadMod(self):
        self.filename=self.askPathDir("Select the path folder of the mod.")
        self.modsPath+=[self.filename]
        self.reloadList()
        self.savePrefs()
        None
    def onDoubleClickListBox(self,event):
        w = event.widget
        if(len(w.curselection())==0):
            return
        
        index = int(w.curselection()[0])
        value = w.get(index)
        if(value in self.modsPath):
            self.modsPath.remove(value)

        self.reloadList()
        self.savePrefs()

        
        
    def onKeyRelease(self,event):
         # If the user is on an entry / input field, skip the event.
        if(CommonFunctions.checkIfInputField(type(self.focus_get()))):
            return  
        
        if(event.char=='d'):
            self.loadMod()
        

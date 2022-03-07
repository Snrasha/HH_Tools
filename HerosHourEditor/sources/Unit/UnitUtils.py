import tkinter as tk
import tkinter.ttk as ttk
import Utils.CommonFunctions as CommonFunctions
import Utils.CommonClass as CommonClass
import Utils.ToolTipFactory as ToolTipFactory

tooltipProjec="Projectiles used per the unit. Bullet Projectile is straight line."

tooltipAttack="Set the range of the attack. Tower give infinite range but become immobile"

attacks={"Melee":"This creature do melee attack","Ranged":"This creature is able to fire a projectile, damaging enemies at a distance.It deals half its normal damage in melee combat,and there is an area where units are too close for ranged attacks and too far for melee attacks.","Long Ranged":"This creature's ranged attacks can strike enemies further away than other ranged creatures would","Short Ranged":"This creature's ranged attacks have a shorter range than other ranged creatures, but can also hit enemies closer to them","Tower":"This creature is unable to move but has infinite range"}

tooltipSpell="Doublie click for add/remove.\n [Alt] for base + upgraded list.\n Right Double click after have select a spell for add to the second list"



class FieldAttackRange(CommonClass.Field):
    def __init__(self,master,side=tk.TOP,**kwargs):
        CommonClass.Field.__init__(self,master,"Attack")
        self.entry.bind("<Button-1>",self.onEnter)
        
        label=ttk.Label(self,text="Upg.")
        label.pack(side=tk.RIGHT,padx=5,pady=5)
        self.entryUnUpgr=tk.Entry(self, font='bold',width=10)
        self.entryUnUpgr.pack(side=tk.RIGHT,padx=5)
        self.entryUnUpgr.bind("<Button-1>",self.onEnter)
        
        self.params=["Melee","None"]
        self.paramsUpgr=["Melee","None"]
        self.set(self.params[0])
        self.set2(self.params[0])
        self.neutral=0
    def setNeutral(self,neutral):
        self.neutral=neutral
        if(neutral==0):
            self.entry.configure(state=tk.NORMAL)
        else:
            self.entry.configure(state=tk.DISABLED)
        
    def onEnter(self,event):
        self.entry.configure(state=tk.DISABLED)
        self.entryUnUpgr.configure(state=tk.DISABLED)
        AttackRangePopup(self,"Attack",event.x_root,event.y_root)

    def getParams(self):
        return (self.params,self.paramsUpgr)
    def setParams(self,params,paramsUpgr):
        self.params=params
        self.paramsUpgr=paramsUpgr
        if(self.params!=None):
            self.set2(self.params[0].replace("anged","")+":"+self.params[1].replace("rojectile",""))  
        if(self.paramsUpgr!=None):
            self.set(self.paramsUpgr[0].replace("anged","")+":"+self.paramsUpgr[1].replace("rojectile",""))        
    def set2(self,text):
        self.entryUnUpgr.delete(0, tk.END)
        if(text==None):
            return
        self.entryUnUpgr.insert(0,text)
        
class AttackRangePopup(CommonClass.Popup):
    def __init__(self,field,title,x,y):
        height=250
        if(field.neutral==1):
            height=150
        CommonClass.Popup.__init__(self,field,title,x,y,width=600,height=height)
        self.field=field

        self.projs=CommonFunctions.readProjectiles()

        self.params,self.paramsUpgr=self.field.getParams()
        frame=ttk.Frame(self,relief="sunken",borderwidth=1,padding=(5,5))
        frame.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,pady=5)
        frame2=ttk.Frame(self,relief="sunken",borderwidth=1,padding=(5,5))
        frame2.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,pady=5,expand=True)

        self.attackmenu=CommonClass.OptionMenu(frame,"Attack Range:",attacks,tooltipAttack,command=self.attack_changed)
        self.projmenu=CommonClass.OptionMenu(frame,"Projectile:",self.projs,tooltipProjec,command=self.proj_changed)
        self.customProj=CommonClass.Field(frame,titleField="Custom Proj:",hintField="")


        self.attackmenu.set(self.params[0])
        if(self.params[1] in self.projs):
            self.projmenu.set(self.params[1])
            self.customProj.entry.configure(state=tk.DISABLED)
        else:
            self.projmenu.set("Custom")
            self.customProj.entry.configure(state=tk.NORMAL)
            self.customProj.set(self.params[1])
        if (self.attackmenu.get()=="Melee"):
            self.projmenu.optionMenu.configure(state=tk.DISABLED)
        if(self.field.neutral==0):
            self.attackmenuUpgr=CommonClass.OptionMenu(frame,"Attack Range Upgr:",attacks,tooltipAttack,command=self.attack_changed2)
            self.projmenuUpgr=CommonClass.OptionMenu(frame,"Projectile:",self.projs,tooltipProjec,command=self.proj_changed2)
            self.customProjUpgr=CommonClass.Field(frame,titleField="Custom Proj:",hintField="")
            self.attackmenuUpgr.set(self.paramsUpgr[0])
            if(self.paramsUpgr[1] in self.projs):
                self.projmenuUpgr.set(self.paramsUpgr[1])
                self.customProjUpgr.entry.configure(state=tk.DISABLED)
            else:
                self.projmenuUpgr.set("Custom")
                self.customProjUpgr.entry.configure(state=tk.NORMAL)
                self.customProjUpgr.set(self.paramsUpgr[1])
            if (self.attackmenuUpgr.get()=="Melee"):
                self.projmenuUpgr.optionMenu.configure(state=tk.DISABLED)            
        
        self.labelDesc=ttk.Label(frame2,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.TOP,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)

        self.labelDesc.configure(text=attacks[self.attackmenu.get()])
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
        self.bind('<Escape>', self.onEscape)        
        
    def attack_changed(self,event):
        if (self.attackmenu.get()=="Melee"):
            self.projmenu.optionMenu.configure(state=tk.DISABLED)
        else:
            self.projmenu.optionMenu.configure(state=tk.NORMAL)
        self.labelDesc.configure(text=attacks[self.attackmenu.get()])
    def attack_changed2(self,event):
        if (self.attackmenuUpgr.get()=="Melee"):
            self.projmenuUpgr.optionMenu.configure(state=tk.DISABLED)
        else:
            self.projmenuUpgr.optionMenu.configure(state=tk.NORMAL)
        self.labelDesc.configure(text=attacks[self.attackmenuUpgr.get()])
    def proj_changed(self,event):
        if (self.projmenu.get()=="Custom"):
            self.customProj.entry.configure(state=tk.NORMAL)
        else:
            self.customProj.entry.configure(state=tk.DISABLED)
        self.labelDesc.configure(text=self.projs[self.projmenu.get()])
    def proj_changed2(self,event):
        if (self.projmenuUpgr.get()=="Custom"):
            self.customProjUpgr.entry.configure(state=tk.NORMAL)
        else:
            self.customProjUpgr.entry.configure(state=tk.DISABLED)
        self.labelDesc.configure(text=self.projs[self.projmenuUpgr.get()])
              
    def onEscape(self,event=None):
        if(self.field.neutral==0):
            self.field.entry.configure(state=tk.NORMAL)
        self.field.entryUnUpgr.configure(state=tk.NORMAL)

        params=[self.attackmenu.get()]
        if(self.projmenu.get()=="Custom"):
            params+=[self.customProj.get()]
        else:
            params+=[self.projmenu.get()]
        if(self.field.neutral==0):
            paramsUpgr=[self.attackmenuUpgr.get()]
            if(self.projmenuUpgr.get()=="Custom"):
                paramsUpgr+=[self.customProjUpgr.get()]
            else:
                paramsUpgr+=[self.projmenuUpgr.get()]
        else:
            paramsUpgr=None

        
        self.field.setParams(params,paramsUpgr)
        self.destroy()

class FieldSpell(CommonClass.Field):
    def __init__(self,master,side=tk.TOP,**kwargs):
        CommonClass.Field.__init__(self,master,"Spells")
        self.entry.bind("<Button-1>",self.onEnter)
        
        label=ttk.Label(self,text="Upg.")
        label.pack(side=tk.RIGHT,padx=5,pady=5)
        self.entryUnUpgr=tk.Entry(self, font='bold',width=10)
        self.entryUnUpgr.pack(side=tk.RIGHT,padx=5)
        self.entryUnUpgr.bind("<Button-1>",self.onEnter)
        
        self.params=[]
        self.paramsUpgr=[]
        self.set("None")
        self.set2("None")
        self.neutral=0
    def setNeutral(self,neutral):
        self.neutral=neutral
        if(neutral==0):
            self.entry.configure(state=tk.NORMAL)
        else:
            self.entry.configure(state=tk.DISABLED)
        
    def onEnter(self,event):
        self.entry.configure(state=tk.DISABLED)
        self.entryUnUpgr.configure(state=tk.DISABLED)
        SpellsPopup(self,"Spells",event.x_root,event.y_root)

    def getParams(self):
        return (self.params,self.paramsUpgr)
    def setParams(self,params,paramsUpgr):
        self.params=params
        self.paramsUpgr=paramsUpgr
        if(self.params!=None):
            self.set2(str(self.params)[1:-1])
        else:
            self.set2("None")
        if(self.paramsUpgr!=None):
            self.set(str(self.paramsUpgr)[1:-1])
        else:
            self.set("None")
    def set2(self,text):
        self.entryUnUpgr.delete(0, tk.END)
        if(text==None):
            return
        self.entryUnUpgr.insert(0,text)

class SpellsPopup(CommonClass.Popup):
    def __init__(self,field,title,x,y):
        width=800
        if(field.neutral==1):
            width=600
            
        CommonClass.Popup.__init__(self,field,title,x,y,width=width,height=200)
        self.field=field

        self.spells=CommonFunctions.readSpells()

        self.params,self.paramsUpgr=self.field.getParams()
        frame=ttk.Frame(self,relief="sunken",borderwidth=1,padding=(5,5))
        frame.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,pady=5)
        frame2=ttk.Frame(self,relief="sunken",borderwidth=1,padding=(5,5))
        frame2.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,pady=5,expand=True)

        
        self.listboxSpell = tk.Listbox(frame)
        self.listboxSpell.bind('<Double-Button-1>', self.onDoubleClickSpell)
        if(self.field.neutral==0):
            self.listboxSpell.bind('<Double-Button-3>', self.onDoubleClickSpell)

        self.listboxSpell.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,expand=True)
        self.listboxSpell.bind('<<ListboxSelect>>', self.onSelectListBox)

        first=None
        for item in self.spells.keys():
            if(first==None):
                first=item
            self.listboxSpell.insert( tk.END, item)

        self.params,self.paramsUpg=self.field.getParams()

        
        self.listbox1 = tk.Listbox(frame)
        self.listbox1.bind('<Double-Button-1>', self.onDoubleClickList1)
        self.listbox1.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,expand=True)
        for item in self.params:
            self.listbox1.insert( tk.END, item)
        if(self.field.neutral==0):
            self.listbox2 = tk.Listbox(frame)
            self.listbox2.bind('<Double-Button-1>', self.onDoubleClickList2)
            self.listbox2.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,expand=True)
            for item in self.paramsUpg:
                self.listbox2.insert( tk.END, item)
        
        self.labelDesc=ttk.Label(frame2,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.TOP,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)
        self.labelDesc.configure(text=tooltipSpell)
        self.labelDesc=ttk.Label(frame2,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.TOP,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)

        

        self.labelDesc.configure(text=self.spells[first])
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
        self.bind('<Escape>', self.onEscape)

            
    def onSelectListBox(self,event):
        w = event.widget
        if(len(w.curselection())==0):
            return
        index = int(w.curselection()[0])
        value = w.get(index)
        self.labelDesc.configure(text=self.spells[value])
        
    def onDoubleClickSpell(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        if(event.num==1):
            if(value not in self.params):
                self.listbox1.insert(tk.END, value)
                self.params+=[value]
            if(event.state==131080 and self.field.neutral==0):
                if(value not in self.paramsUpg):
                    self.listbox2.insert( tk.END, value)
                    self.paramsUpg+=[value]
        elif(event.num==3):
            if(event.state==131080 and value not in self.params):
                self.listbox1.insert(tk.END, value)
                self.params+=[value]
            if(self.field.neutral==0 and value not in self.paramsUpg):
                self.listbox2.insert( tk.END, value)
                self.paramsUpg+=[value]           
                    
    def onDoubleClickList1(self,event):
        w = event.widget
        
        index = int(w.curselection()[0])
        value = w.get(index)
        if(value in self.params):
            self.params.remove(value)

        self.listbox1.delete(0, tk.END)
        for item in self.params:
            self.listbox1.insert( tk.END, item)
        if(event.state==131080 and self.field.neutral==0):
            if(value in self.paramsUpg):
                self.paramsUpg.remove(value)
                
            self.listbox2.delete(0, tk.END)
            for item in self.paramsUpgr:
                self.listbox2.insert(tk.END, item)
        
    def onDoubleClickList2(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        if(event.state==131080):
            if(value in self.params):
                self.params.remove(value)

            self.listbox1.delete(0, tk.END)
            for item in self.params:
                self.listbox1.insert( tk.END, item)
        
        if(value in self.paramsUpg):
            self.paramsUpg.remove(value)
            
        self.listbox2.delete(0, tk.END)
        for item in self.paramsUpgr:
            self.listbox2.insert(tk.END, item)        
        
    
    def onEscape(self,event=None):
        if(self.field.neutral==0):
            self.field.entry.configure(state=tk.NORMAL)
        self.field.entryUnUpgr.configure(state=tk.NORMAL)

        self.field.setParams(self.params,self.paramsUpgr)
        self.destroy()

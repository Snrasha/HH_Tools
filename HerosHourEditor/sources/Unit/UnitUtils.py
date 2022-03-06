import tkinter as tk
import tkinter.ttk as ttk
import Utils.CommonFunctions as CommonFunctions
import Utils.CommonClass as CommonClass
import Utils.ToolTipFactory as ToolTipFactory

tooltipProjec="Projectiles used per the unit. Bullet Projectile is straight line."

tooltipAttack="Set the range of the attack. Tower give infinite range but become immobile"

attacks={"Melee":"This creature do melee attack","Ranged":"This creature is able to fire a projectile, damaging enemies at a distance.It deals half its normal damage in melee combat,and there is an area where units are too close for ranged attacks and too far for melee attacks.","Long Ranged":"This creature's ranged attacks can strike enemies further away than other ranged creatures would","Short Ranged":"This creature's ranged attacks have a shorter range than other ranged creatures, but can also hit enemies closer to them","Tower":"This creature is unable to move but has infinite range"}




class FieldAttackRange(CommonClass.Field):
    def __init__(self,master,side=tk.TOP,**kwargs):
        CommonClass.Field.__init__(self,master,"Attack Range")
        self.entry.bind("<Button-1>",self.onEnter)
        self.params=["Melee","None"]
        
    def onEnter(self,event):
        self.entry.configure(state=tk.DISABLED)
        AttackRangePopup(self,"Attack",event.x_root,event.y_root)

    def getParams(self):
        return self.params
    def setParams(self,params):
        self.params=params
        
class AttackRangePopup(CommonClass.Popup):
    def __init__(self,field,title,x,y):
        CommonClass.Popup.__init__(self,field,title,x,y,width=600)
        self.field=field

        self.projs=CommonFunctions.readProjectiles()

        self.params=self.field.getParams()
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
            
        
        self.labelDesc=ttk.Label(frame2,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.TOP,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)

        self.labelDesc.configure(text=attacks[self.attackmenu.get()])
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
        self.bind('<Escape>', self.onEscape)        
        
    def attack_changed(self,event):
##        print(self.attackmenu.get())
        if (self.attackmenu.get()=="Melee"):
            self.projmenu.optionMenu.configure(state=tk.DISABLED)
        else:
            self.projmenu.optionMenu.configure(state=tk.NORMAL)
        self.labelDesc.configure(text=attacks[self.attackmenu.get()])

    def proj_changed(self,event):
##        print(self.projmenu.get())
        if (self.projmenu.get()=="Custom"):
            self.customProj.entry.configure(state=tk.NORMAL)
        else:
            self.customProj.entry.configure(state=tk.DISABLED)
        self.labelDesc.configure(text=self.projs[self.projmenu.get()])
        
    def onEscape(self,event=None):
        self.field.entry.configure(state=tk.NORMAL)
        self.field.set(self.attackmenu.get())
        params=[self.attackmenu.get()]
        if(self.projmenu.get()=="Custom"):
            params+=[self.customProj.get()]
        else:
            params+=[self.projmenu.get()]

        
        self.field.setParams(params)
        self.destroy()

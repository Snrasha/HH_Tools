import tkinter as tk
import tkinter.ttk as ttk
import os
import Hero.HeroTab as HeroTab
import Faction.FactionTab as FactionTab
import Unit.UnitTab as UnitTab
import Mods.ModTab as ModTab

import Utils.CommonClass as CommonClass
import Utils.CommonFunctions as CommonFunctions





# Empty tab for work in progress.
class EmptyTab(CommonClass.Tab):     
    def  __init__(self,master,window):
        CommonClass.Tab.__init__(self,master,window)
        self.pack(fill=tk.BOTH,expand=True)
        label=ttk.Label(self,text="Work in progress")
        label.pack(fill=tk.BOTH,expand=True,padx=5,pady=5)
    def onKeyRelease(self,event):
        None
    def bindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)
    def unBindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)

class Application(ttk.Notebook):
    def  __init__(self,window):
        ttk.Notebook.__init__(self,window)
        style = ttk.Style(window)
        style.theme_use('clam')
        style.configure('TNotebook.Tab', width=window.winfo_screenwidth())
##        style.configure('TMenubutton.Menubutton', background="red")
##        style.configure('TMenubutton',w=2, background="red")
##        style.configure('TMenubutton.Button', background="red")
##        style.configure('TMenubutton.Label', background="red")

##        style.configure('TFrame', highlightthickness=0)
##        style.configure('TLabelframe', background="white")
##        style.configure('TLabelframe.Label', background="white")
##        style.configure('TFrame', background="white")
##        style.configure('TLabel',background="white")
##        style.configure('TLabelframe' , bordercolor="black")
       
        

        
        self.window=window
        self.pack(fill=tk.BOTH,expand=True)
        self.tabs=[]

        # Add Tabs.
        self.modtab=ModTab.ModLoad(self,window)
        self.currentTab=self.modtab.currentTab
        self.tabs+=[self.modtab]
        self.tabs+=[FactionTab.TabFactionEditor(self,window)]
        self.tabs+=[HeroTab.TabHeroEditor(self,window)]
        self.tabs+=[UnitTab.TabUnitEditor(self,window)]

##        self.tabs+=[EmptyTab(self,window)]
##        self.tabs+=[EmptyTab(self,window)]
        
        

        self.window.bind("<KeyPress>", self.onKeyDown)
        self.window.bind('<Escape>', self.onEscape)
        self.bind("<<NotebookTabChanged>>", self.onTabChanged)

        self.add(self.tabs[0],text="Mods (1)")
        self.add(self.tabs[1],text="Faction (2)")
        self.add(self.tabs[2],text="Hero (3)")
        self.add(self.tabs[3],text="Unit (4)")
##        self.add(self.tabs[4],text="Artifact (5)")
##        self.add(self.tabs[5],text="Hero classes (6)")

        self.changeTab(self.currentTab)

    def onEscape(self,event):
        # Exit the input field or any Entry
        self.window.focus()
    def onTabChanged(self,event):
        tab = event.widget.tab('current')["text"]
        
        self.changeTab(tab[-2])
        self.window.focus()


    # Switch the tab and disable key listener of the old tab and enable for the new tab.
    def onKeyDown(self,event):
        if(len(event.char)!=1):
            return
        # If the user is on an entry / input field, skip the event.
        if(CommonFunctions.checkIfInputField(type(self.focus_get()))):
            # When press Enter, remove the focus if Entry.
            if(ord(event.char)==13):
                self.window.focus()
            return


        self.changeTab(event.char)
    def changeTab(self,char):
        ordinal=ord(char)
        # begin to 49 for '1'
        for i in range(len(self.tabs)):
            if(ordinal== 49+i):
                self.currentTab=char
                self.unBindKeyTabs()
                self.select(self.tabs[i])
                self.tabs[i].bindKey() 
            
    def unBindKeyTabs(self):
        for i in range(0,len(self.tabs)):
            self.tabs[i].unBindKey()        
    def onClosing(self):
        self.modtab.savePrefs(self.currentTab)
        self.window.destroy()

## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title("Hero's hour Editor | Version 1.1b | 09 april 2022 | Ping Snrasha for any feedback, idea or typo.")
        self.geometry("1200x450+100+300")
        
        app=Application(self)
        self.protocol("WM_DELETE_WINDOW", app.onClosing)
        

if __name__ == '__main__':
##    CommonFunctions.writeAllData()
    windows = Windows()
    windows.mainloop()

import tkinter as tk
import tkinter.ttk as ttk
import os
import Hero.HeroTab as HeroTab
import Utils.CommonClass as CommonClass

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
        style.configure('TNotebook.Tab', width=window.winfo_screenwidth())

        self.window=window
        self.pack(fill=tk.BOTH,expand=True)
        self.tabs=[]

        # Add Tabs.
        self.tabs+=[HeroTab.TabHeroEditor(self,window)]
        self.tabs+=[EmptyTab(self,window)]
        self.tabs+=[EmptyTab(self,window)]
##        self.tabs+=[FactionTab.TabFactionEditor(self,window)]
        self.tabs+=[EmptyTab(self,window)]
        
        self.tabs[0].bindKey()

        self.window.bind("<KeyPress>", self.onKeyDown)
        self.window.bind('<Escape>', self.onEscape)
        
        self.add(self.tabs[0],text="Hero (1)")
        self.add(self.tabs[1],text="Unit (2)")
        self.add(self.tabs[2],text="Faction (3)")
        self.add(self.tabs[3],text="Artifact (4)")

    def onEscape(self,event):
        # Exit the input field or any Entry
        self.window.focus()


    # Switch the tab and disable key listener of the old tab and enable for the new tab.
    def onKeyDown(self,event):

        # If the user is on an entry / input field, skip the event.
        if(type(self.focus_get()) == tk.Entry or type(self.focus_get()) == ttk.Entry):
            # When press Enter, remove the focus if Entry.
            if(ord(event.char)==13):
                self.window.focus()
            return            
        
        if(event.char=='1'):
            self.unBindKeyTabs()
            self.select(self.tabs[0])
            self.tabs[0].bindKey()
        if(event.char=='2'):
            self.unBindKeyTabs()
            self.select(self.tabs[1])
            self.tabs[1].bindKey()
        if(event.char=='3'):
            self.unBindKeyTabs()
            self.select(self.tabs[2])
            self.tabs[2].bindKey()
        if(event.char=='4'):
            self.unBindKeyTabs()
            self.select(self.tabs[3])
            self.tabs[3].bindKey()
            
    def unBindKeyTabs(self):
        for i in range(0,len(self.tabs)):
            self.tabs[i].unBindKey()        


## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title("Hero's hour Editor")
        self.geometry("1200x450+100+300")
        
        app=Application(self)
        

if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os

def removeLineBreak():
    filenameToRead=askFile()
    if(filenameToRead==None or len(filenameToRead.strip())==0):
        return
    filenameToWrite=askSaveFile(filenameToRead)
    file = open(filenameToRead, 'r')
    savefile = open(filenameToWrite, 'w')
    lines=file.readlines()
    file.close()
    l=""
    for line in lines:
        l+=line.strip()
        
    savefile.write(l)
    
    savefile.close()


def askFile():
    filename=fd.askopenfilename(title="Select a file for remove linebreak",filetypes=[("JS files","*.js")])
    if(filename==None or filename.strip()==""):
        filename=None
    return filename
## Call the save dialog
def askSaveFile(oldFilename):
    
    
    inifile=oldFilename.split('/')[-1]
    inifile=inifile[:-len(".js")]+" copy.js"
    
        
    filename=fd.asksaveasfilename(initialfile=inifile,title="Copy of the file",filetypes=[("JS files","*.js")])
    if(len(filename.strip())==0):
        filename=None 
    elif not filename.endswith(".js"):
        filename+=".js"
    return filename


   
class Application(ttk.Frame):
    def  __init__(self,window):
        ttk.Frame.__init__(self,window)
        self.window=window

        style = ttk.Style(window)
        style.theme_use('clam')
        self.window.bind("<KeyRelease>", self.onKeyRelease)

        self.pack(fill=tk.BOTH,expand=True)
        label=ttk.Label(self,text="Click the D hotkey. Will remove every linebreak.",wraplength=300)
        label.pack(fill=tk.BOTH,side=tk.TOP,padx=5,pady=5)
        

    def onKeyRelease(self,event):
        print(event)
        if(event.char=='d'):
            removeLineBreak()

## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        super().__init__()

        # root window
        self.title("Wiki Auto-Remove LineBreak")
        self.geometry("300x50+300+300")
        app=Application(self)
        
if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()



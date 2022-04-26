import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import os

def removeLineBreak():
    filenameToRead=askFile("Select a file for remove linebreak")
    if(filenameToRead==None or len(filenameToRead.strip())==0):
        return
    filenameToWrite=askSaveFile(filenameToRead,"Compiled")
    file = open(filenameToRead, 'r')
    savefile = open(filenameToWrite, 'w')
    lines=file.readlines()
    file.close()
    l=""
    for line in lines:
        l+=line.strip()
        
    savefile.write(l)
    
    savefile.close()


def askFile(title):
    filename=fd.askopenfilename(title=title,filetypes=[("JS files","*.js")])
    if(filename==None or filename.strip()==""):
        filename=None
    return filename
## Call the save dialog
def askSaveFile(oldFilename,copySuffix):
    
    
    inifile=oldFilename.split('/')[-1]
    inifile=inifile[:-len(".js")]+" "+copySuffix+".js"
    
        
    filename=fd.asksaveasfilename(initialfile=inifile,title=copySuffix+" file",filetypes=[("JS files","*.js")])
    if(len(filename.strip())==0):
        filename=None 
    elif not filename.endswith(".js"):
        filename+=".js"
    return filename
class Parser():
    def  __init__(self):
        self.filenameToRead=askFile("Select a file for add linebreak")
        if(self.filenameToRead==None or len(self.filenameToRead.strip())==0):
            return
        self.filenameToWrite=askSaveFile(self.filenameToRead,"Uncompiled")

        self.lines=[]
        self.index=0
        self.isInStringOne=False
        self.isInStringTwo=False
        self.nbTab=0
        self.currentLen=1
        self.length=0
        self.fileLines=""
    def addLineBreak(self):
        if(self.filenameToRead==None):
            return
        if(self.filenameToWrite==None):
            return        
        
        file = open(self.filenameToRead, 'r')
        lines=file.readlines()
        file.close()
        for line in lines:
            self.fileLines+=line.strip()

        self.length=len(self.fileLines)
        
        while(self.index< self.length):
##            print(self.getChar())
            
            if(self.checkChar('\'') and not self.isInStringTwo):
                self.isInStringOne=not self.isInStringOne
            if(self.checkChar('\"') and not self.isInStringOne):
                self.isInStringTwo=not self.isInStringTwo
            if(self.isInStringOne or self.isInStringTwo):
                if(self.checkChar('<')):
                    self.fillTree()
                    
            elif(self.checkChar('{') or self.checkChar('[')):
                self.addLine()
                self.nbTab+=1
            elif(self.checkChar('}') or self.checkChar(']')):
                self.nbTab-=1
            elif(self.checkChar(',') or self.checkChar(';')):
                self.addLine()      
            self.currentLen+=1
            self.index+=1
        self.addLine()
        
        self.save()

    def fillTree(self):
        tag,tagStart,idx,isEndTag=self.getNextTag()
        if(tag==None):
            return
        
        self.currentLen-=1
        self.index-=1
        self.addLine()
        self.index+=1
        tree=Tree()
        while(self.index< self.length):
##            print(" "+self.getChar())
            if(self.checkChar('\'') and not self.isInStringTwo):
                self.isInStringOne=not self.isInStringOne
                break
            if(self.checkChar('\"') and not self.isInStringOne):
                self.isInStringTwo=not self.isInStringTwo
                break
            if(self.checkChar('<')):
                tag,tagStart,idx,isEndTag=self.getNextTag()
                
                if(tag==None or tag.upper()=="BR"):
                    None
                else:
                    content=self.fileLines[(self.index-self.currentLen+1):self.index]
                    self.currentLen=0
                    tree.addContent(content)
                    if(isEndTag == 2):
                        tree.goToParentTag()
                    elif (isEndTag==1):
                        tree.addTagAndGotToChild("<"+tagStart[:-1]+">",tag)
                        tree.goToParentTag()
                    else:
                        tree.addTagAndGotToChild("<"+tagStart+">",tag)
                    self.index+=idx
                    
            self.currentLen+=1
            self.index+=1            
        self.currentLen=1
##        self.index-=1
        self.lines+=[tree.toString(self.nbTab)]
        
        
    def getNextTag(self):
        idx=1
        tag=""
        stopAdd=False
        tagEnd=0
        while(self.index+idx< self.length):
            
            # The tag is a end tag
            if(self.getChar(idx)=='/' and idx==1):
                tagEnd=2
                idx+=1
                continue
            # In this case, not a tag if begin per anything else than a letter
            if(idx==1):
                char=self.getChar(idx).lower()
                if(char>='a' and char<='z'):
                    None
                else:
                    return (None,None,None,False)
            
            if(self.getChar(idx)==' '):
                stopAdd=True
            if(self.getChar(idx)=='>'):
                if(self.getChar(idx-1)=='/'):
                    tagEnd=1
                    tag=tag[:-1]
                
                return (tag,self.fileLines[self.index+1:self.index+idx],idx,tagEnd)
            if(not stopAdd):
                tag+=self.getChar(idx)
            idx+=1

    def save(self):
        savefile = open(self.filenameToWrite, 'w')
        for line in self.lines:
            savefile.write(line+"\n")  
        savefile.close()
    def checkChar(self,char):
        return self.getChar()==char

    def getChar(self,idx=0):
        return self.fileLines[self.index+idx]
    def addLine(self):
        self.lines+=['\t'*self.nbTab+self.fileLines[(self.index-self.currentLen)+1:self.index+1]]

        self.currentLen=0

class Tree():
    def  __init__(self):
        self.currentTag=Tag(None,"root","root")
        self.currentTag.parent=self.currentTag
    def addTagAndGotToChild(self,tagStart,tagEnd):
        self.currentTag=self.currentTag.addChild(tagStart,tagEnd,None)
    def addContent(self,content):
        self.currentTag.addChild(None,None,content)
    def goToParentTag(self):
        self.currentTag=self.currentTag.parent
    def toString(self,level):
        while(self.currentTag!=self.currentTag):
            self.goToParentTag()
        string=""
        for child in self.currentTag.childs:    
            string+=child.toString(level)
        return string
    
        
class Tag():
    def  __init__(self,parent,tagStart,tagEnd,content=None):
        self.tagStart=tagStart
        self.tagEnd=tagEnd
        self.childs=[]
        self.content=content
        self.parent=parent
    def addChild(self,tagStart,tagEnd,content):
        self.childs+=[Tag(self,tagStart,tagEnd,content)]
        return self.childs[-1]
        
    def toString(self,level):
        if(self.tagStart==None):
            if(len(self.content.strip())==0):
                return ""
            return '\t'*level+self.content+"\n"
        string=""
        stringChild=""
        for child in self.childs:
            stringChild+=child.toString(level+1)
        
        if(len(stringChild.strip())>0):
            string+='\t'*level+self.tagStart+"\n"
        else:
            string+='\t'*level+self.tagStart[:-1]+"/>\n"
            return string
        string+=stringChild
        
        string+='\t'*level+"</"+self.tagEnd+">\n"
        return string
        
        
class Application(ttk.Frame):
    def  __init__(self,window):
        ttk.Frame.__init__(self,window)
        self.window=window

        style = ttk.Style(window)
        style.theme_use('clam')
        self.window.bind("<KeyRelease>", self.onKeyRelease)

        self.pack(fill=tk.BOTH,expand=True)
        label=ttk.Label(self,text="Click 'D' hotkey. Will remove every linebreak.\nClick 'U' hotkey for a opposite operation",wraplength=300)
        label.pack(fill=tk.BOTH,side=tk.TOP,padx=5,pady=5)
        
    def onKeyRelease(self,event):
        if(event.char=='d'):
            removeLineBreak()
        if(event.char=='u'):
            Parser().addLineBreak()
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



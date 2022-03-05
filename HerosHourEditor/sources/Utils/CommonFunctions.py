from PIL import Image,ImageTk
from tkinter import filedialog as fd
import tkinter as tk
import tkinter.ttk as ttk
import os
import Utils.Skills as Skills


## For have a unique software without any data around, we transform the csv to a python data. We call never this function except for update the data.
def writePythonData(descriptionsSkill,file):
    backup = open("Skill.py", 'w')
    backup.write(str(descriptionsSkill))
    backup.close()


## Read the Skills.csv for all name skills followed per their description
def readSkills(csv=False,overwritePythonData=False):
    if(csv):  
        descriptionsSkills={"None":"Click on a skill on the list or the skill tree for get the description"}

        if(os.path.exists("Skills.csv")):
            descriptionsSkills={"None":"Click on a skill on the list or the skill tree for get the description"}
            file1 = open("Skills.csv", 'r')
            lines=file1.readlines()
            for line in lines:
                if(line.startswith('#')):
                   continue
                split=line.split(";")
                descriptionsSkills[split[0]]=split[1]
                
            file1.close()
        else:
            descriptionsSkills={"None":"Skills.csv has not be found. Put the Skills.csv on the same folder."}
        if(overwritePythonData):
            fillSkill(descriptionsSkills,"Skill.py")
        return descriptionsSkills
    else:
        return Skills.get()


## Made a backup of the opened file.
def madeBackUp(backupname,filename):
    file1 = open(filename, 'r')
    lines=file1.readlines()

    backup = open(backupname, 'w')
    backup.writelines(lines)
    
    file1.close()
    backup.close()


## For hero portrait, we add black outline around each pixel.
def addBlackOutline(path):
    image=Image.open(path)
    w=image.size[0]
    h=image.size[1]
    gameImage=Image.new("RGBA", (w, h), (0, 0, 0, 0)) 
    pixels = image.load()
    pixelsBlack=gameImage.load()

    for i in range(w):
        for j in range(h):
            if(pixels[i,j][3]!=0):
                if(j+1<h):
                    pixelsBlack[i, j + 1] = (0, 0, 0, 255)
                if(j-1>=0):
                    pixelsBlack[i, j - 1] = (0, 0, 0, 255)
                if(i+1<w):
                    pixelsBlack[i + 1, j] = (0, 0, 0, 255)
                if(i-1>=0):
                    pixelsBlack[i - 1, j] = (0, 0, 0, 255)
    for i in range(w):
        for j in range(h):
            if(pixels[i,j][3]!=0):
                pixelsBlack[i, j] = pixels[i,j]
                   
    return gameImage

## Call the save dialog
def askSaveFile(oldFilename,title):
    if(oldFilename!=None):
        inifile=oldFilename.split('/')[-1]
    else:
        inifile=None
    
    filename=fd.asksaveasfilename(initialfile=inifile,title=title,filetypes=[("TXT Files","*.txt")])
    if(len(filename.strip())==0):
        filename=None 
    elif not filename.endswith(".txt"):
        filename+=".txt"
    return filename

## Call the open dialog
def askEditFile(title):
    filename=fd.askopenfilename(title=title,filetypes=[("TXT Files","*.txt")])
    if(filename==None or filename.strip()==""):
        filename=None
    return filename

## Add a image to a label.
def addImage(path,label,size,outline=False,side=tk.TOP):
    if(os.path.exists(path)):
        if(outline):
            image = addBlackOutline(path)
        else:
            image=Image.open(path)
        n_image = image.resize((size, size),resample=Image.BOX)
        photo = ImageTk.PhotoImage(n_image)
        setImage(label,photo,side)
    else:
        setBackground(label,size,side=side)
def setBackground(label,size,color= (0, 0, 0, 255),side=tk.TOP):
    
    if not (isinstance(size,tuple)):
        size=(size,size)
        
    photo = ImageTk.PhotoImage(Image.new("RGBA", size, color))
    setImage(label,photo,side)

def setImage(label,photo,side):
    label.image = photo
    label.configure(image=photo)
    label.pack(fill=tk.BOTH,side=side)    



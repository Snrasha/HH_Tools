from PIL import Image,ImageTk
from tkinter import filedialog as fd
import tkinter as tk
import tkinter.ttk as ttk
import os
import Utils.Data as Data
import Utils.CommonClass as CommonClass


# If the user is on an entry / input field, skip the event.
def checkIfInputField(compare):
    return (compare == tk.Text or\
           compare == tk.Entry or\
           compare == ttk.Entry or\
           compare == CommonClass.EntrySimplified)

## For have a unique software without any data around, we transform the csv to a python data. We call never this function except for update the data.
def writePythonData(descSkills,descAbilities,descAbilitiesBis,descProjectiles,descSpells):
    backup = open("Data2.py", 'w')
    backup.write("skills="+str(descSkills)+'\n')
    backup.write("abilities="+str(descAbilities)+'\n')
    backup.write("abilitiesBis="+str(descAbilitiesBis)+'\n')
    backup.write("spells="+str(descSpells)+'\n')
    backup.write("projectiles="+str(descProjectiles)+'\n')
    backup.close()

def writeAllData():
    descSkills=getCSVData("Utils/Skills.csv")
    if(descSkills==None):
        descSkills={"None":"Skills.csv not found"}
    descAbilities=getCSVData("Utils/Abilities.csv")
    if(descAbilities==None):
        descAbilities={"None":"Abilities.csv not found"}
    descAbilitiesBis=getCSVData("Utils/AbilitiesBis.csv")
    if(descAbilitiesBis==None):
        descAbilitiesBis={"None":"AbilitiesBis.csv not found"}
    descProjectiles=getCSVData("Utils/Projectiles.csv")
    if(descProjectiles==None):
        descProjectiles={"None":"Projectiles.csv not found"}
    descSpells=getCSVData("Utils/Spells.csv")
    if(descSpells==None):
        descSpells={"None":"Spells.csv not found"}
    writePythonData(descSkills,descAbilities,descAbilitiesBis,descProjectiles,descSpells)
def getCSVData(file):
    if(os.path.exists(file)):
        datas={}
        file1 = open(file, 'r')
        lines=file1.readlines()
        firstLine=False
        tags=[]
        for line in lines:
            if not firstLine:
                firstLine=True
                tags=line.split(";")
                
            if(line.startswith('#')):
               continue
            split=line.split(";")
            
            length=len(split)
            for i in range(length):
                split[i]=split[i].strip()
            if(length>2 and split[2].lower().startswith("f")):
                continue
            if(length==1):
                datas[split[0]]="//"
            else:
                text=split[1]
                
                if(len(text)>1):
                    text=text[0].upper()+text[1:]
##                else:
##                    print(split[0]+";"+split[1])
                datas[split[0]]=text
                
                for i in range(3,length,1):
                    datas[split[0]]+="\n"+tags[i].strip()+": "+split[i]
        file1.close()
        return datas
    else:
        return None
    


def readSkills():
    return Data.skills
def readAbilities():
    return Data.abilities
def readSpells():
    return Data.spells
def readAbilitiesBis():
    return Data.abilitiesBis
def readProjectiles():
    return Data.projectiles

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



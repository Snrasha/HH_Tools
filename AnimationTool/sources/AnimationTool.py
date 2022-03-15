import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from os import path as pth
from PIL import Image

def askFile():
    filename=fd.askopenfilename(title="Select a spritesheet",filetypes=[("PNG Files","*.png")])
    if(filename==None or filename.strip()==""):
        filename=None
    return filename
## Call the save dialog
def askSaveFile(oldFilename):
    if(oldFilename!=None):
        inifile=oldFilename.split('/')[-1]
    else:
        inifile=None
    if(inifile!=None):
        indx=inifile.rfind('.')
        if(indx!=-1):
            inifile=inifile[0:indx]
    
    filename=fd.asksaveasfilename(initialfile=inifile,title="Save GIF",filetypes=[("GIF Files","*.gif")])
    if(len(filename.strip())==0):
        filename=None 
    elif not filename.endswith(".gif"):
        filename+=".gif"
    return filename

def getImages(path,choice):
    isUnit=False
    images=[]    
    image=Image.open(path)
    image=image.convert('RGBA')
    w=image.size[0]
    h=image.size[1]
    alpha = image.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
    image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    image.paste(255, mask)
    cut=20
    widthImg=w/cut
    if(widthImg==round(widthImg)):
        isUnit=True
    else:
        cut=32
        widthImg=w/cut
    if(widthImg<1):
        return (None,False)
    c=image.getpalette()[-1]
    
    for i in range(0,cut):
        img=image.crop((i*widthImg,0,(i+1)*widthImg,h))
        img2=Image.new("P", (24, 24),255)
        img2.putpalette(image.getpalette())
        Image.Image.paste(img2,img,((24-img.size[0])//2,24-img.size[1]))
        img2=img2.resize((24*6, 24*6),resample=Image.BOX)
        images+=[img2]
    return (images,isUnit)


def toGif(path,choice):
    if not(pth.exists(path)):
        return
    
    imgs,isUnit=getImages(path,choice)
    if(imgs==None):
        return None
    savePath=askSaveFile(path)
    if(savePath==None):
        return None

    if(isUnit):
        idleAnim=[imgs[i] for i in range(0,4)]
        walkAnim=[imgs[i] for i in range(4,8)]
        attackAnim=[imgs[i] for i in range(8,12)]
        hurtAnim=[imgs[i] for i in range(12,16)]
        deathAnim=[imgs[i] for i in range(16,20)]
        imgs=[]

        if(choice[0]==0):
            for i in range(0,4):
                imgs+=idleAnim
            for i in range(0,2):
                imgs+=walkAnim
            imgs+=attackAnim
            for i in range(0,2):
                imgs+=walkAnim
            imgs+=attackAnim
            for i in range(0,4):
                imgs+=idleAnim
            imgs+=hurtAnim
        elif (choice[0] == 1):
            for i in range(0,4):
                imgs+=idleAnim
            imgs+=deathAnim
    else:
        directions=[]
        for i in range(0,8):
            direc=[imgs[i*4+inc] for inc in range(0,4)]
            directions+=[direc]
        imgs=[]
        for i in range(0,8):
            for c in range(0,3):
                imgs+=directions[i]

    if(choice[0]==1):
        imgs[0].save(fp=savePath, format='GIF', append_images=imgs[1:],
        save_all=True, duration=200, transparency=255, disposal=2,optimize=False) 
    else:
        imgs[0].save(fp=savePath, format='GIF', append_images=imgs[1:],
        save_all=True, duration=200, loop=0,transparency=255, disposal=2,optimize=False) 
    
    

#transparency=255, disposal=2,optimize=False) 

description="Set what you want then load a spritesheet.\nFor unit: do idle, walk, attack and hurt.\nIf death only, will display the death without looping.\nFor hero, will display the animation a bit much longer."
            
class Application(ttk.Frame):
    def  __init__(self,window):
        ttk.Frame.__init__(self,window)

        style = ttk.Style(window)
        style.theme_use('clam')

        self.window=window
        self.pack(fill=tk.BOTH,expand=True)
        self.bg = style.lookup('TFrame', 'background')

        frame1=ttk.Frame(self,borderwidth=1,relief="sunken",padding=(5,5))
        frame1.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        frame2=ttk.Frame(self)
        frame2.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3))
        frame3=ttk.Frame(self)
        frame3.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(3,3),pady=(3,3))
        self.checkBoxVar=[]
        self.checkBoxVar+=[tk.IntVar()]
        checkbtn = tk.Checkbutton(frame3,text="Death (No looping)", variable = self.checkBoxVar[0], onvalue = 1, offvalue = 0,bg=self.bg)
        checkbtn.pack(side=tk.TOP)
        self.checkBoxVar+=[tk.IntVar()]
##        checkbtn = tk.Checkbutton(frame3,text="cubic scale", variable = self.checkBoxVar[1], onvalue = 1, offvalue = 0,bg=self.bg)
##        checkbtn.pack(side=tk.TOP)
        button=ttk.Button(frame2,text="Open",command=self.onClick)
        button.pack(fill=tk.BOTH,side=tk.TOP)
        
  
        label=ttk.Label(frame1,text=description)
        label.pack(fill=tk.BOTH,side=tk.TOP)

        self.window.bind('<Escape>', self.onClosing)


        
    def onClosing(self,event=None):
        self.window.destroy()

    def onClick(self):
        filename=askFile()
        if(filename!=None):
            choice=[0,0]
            if(self.checkBoxVar[0].get()==1):
                choice[0]=1
            
            toGif(filename,choice)
            return




## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        
        super().__init__()
        # root window
        self.title("Hero's Hour Tool Animation")
        self.geometry("400x120+300+300")
        
        app=Application(self)
        self.protocol("WM_DELETE_WINDOW", app.onClosing)
        
if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()



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

    if not inifile.endswith(" Animation"):
        inifile+=" Animation"

    if not inifile.endswith(".gif"):
        inifile+=".gif"
    
    filename=fd.asksaveasfilename(initialfile=inifile,title="Save GIF",filetypes=[("GIF Files","*.gif")])
    if(len(filename.strip())==0):
        filename=None 
    elif not filename.endswith(".gif"):
        filename+=".gif"
    return filename

def getImages(path,choice):
    images=[]    
    image=Image.open(path)
    image=image.convert('RGBA')
    w=image.size[0]
    h=image.size[1]
    if(choice[0]==1):
        pixels = image.load()
        insertGray=[False,0,0]
        for i in range(h):
            if(insertGray[0]):
                break
            for j in range(w):
                if(pixels[j,i][3]==0):
                    pixels[j,i]=(180,180,180,255)
                    insertGray=[True,j,i]
                    break
                
    alpha = image.split()[3]
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
    image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
    image.paste(255, mask)
    cut=20
    if(choice[3]):
        cut=32
    widthImg=w/cut
    
    if(widthImg<1):
        return None
    
    c=image.getpalette()[-1]
    if(choice[0]==1):
        pixels = image.load()
        grayColor=pixels[insertGray[1],insertGray[2]]
        pixels[insertGray[1],insertGray[2]]=255
    

    for i in range(0,cut):
        img=image.crop((i*widthImg,0,(i+1)*widthImg,h))
        scal=choice[2]
        if(choice[1]==1):
            if(choice[0]==0):
                img2=Image.new("P", (24, 24),255)
                img2.putpalette(image.getpalette())
                Image.Image.paste(img2,img,((24-img.size[0])//2,24-img.size[1]))
                img=img2.resize((img2.size[0]*scal, img2.size[1]*scal),resample=Image.BOX)
            if(choice[0]==1):
                img2=Image.new("P", (48, 24),255)
                img2.putpalette(image.getpalette())
                Image.Image.paste(img2,img,((24-img.size[0])//2,24-img.size[1]))
                Image.Image.paste(img2,img,(24+(24-img.size[0])//2,24-img.size[1]))
                pixels = img2.load()
                for i in range(24,48):
                    for j in range(24):
                        if(pixels[i,j]==255):
                            pixels[i,j]=grayColor
                            
                img=img2.resize((img2.size[0]*scal, img2.size[1]*scal),resample=Image.BOX)
        else:
            if(choice[0]==0):
                img=img.resize((img.size[0]*scal, img.size[1]*scal),resample=Image.BOX)
            if(choice[0]==1):
                img2=Image.new("P", (widthImg*2, h),255)
                img2.putpalette(image.getpalette())
                Image.Image.paste(img2,img,(0,0))
                Image.Image.paste(img2,img,(widthImg,0))
                pixels = img2.load()
                for i in range(widthImg,widthImg*2):
                    for j in range(h):
                        if(pixels[i,j]==255):
                            pixels[i,j]=grayColor
        images+=[img]
        
    return images


def toGif(path,choice):
    if not(pth.exists(path)):
        return
    
    imgs=getImages(path,choice)
    if(imgs==None):
        return None
    savePath=askSaveFile(path)
    if(savePath==None):
        return None

    if (not choice[3]):
        # Put one black pixel on the bottom left for the death animation.
        for img in imgs:
            pixels = img.load()
            if(pixels[0,img.size[1]-1] == 255):
                pixels[0,img.size[1]-1]=0
            
        idleAnim=[imgs[i//2+0] for i in range(8)]
        walkAnim=[imgs[i//2+4] for i in range(8)]
        attackAnim=[imgs[i+8] for i in range(4)]
        hurtAnim=[imgs[i//2+12] for i in range(8)]
        deathAnim=[imgs[i//2+16] for i in range(8)]
        listo=[idleAnim,walkAnim,attackAnim,hurtAnim,deathAnim]
        imgs=[]


        animationlist=[0,0,0,1,1,0,2,0,3,0,2,0,2,3,0,1,1,0,0,0,0,1,1,0,2,0,3,0,2,0,2,3,0,1,1,0,4]
        for i in animationlist:
            imgs+=listo[i]
        for i in range(0,20):
            imgs+=[deathAnim[-1]]        

    else:
        directions=[]
        for i in range(0,8):
            direc=[imgs[i*4+inc] for inc in range(0,4)]
            directions+=[direc]
        imgs=[]
        for i in range(0,8):
            for c in range(0,3):
                imgs+=directions[i]


    imgs[0].save(fp=savePath, format='GIF', append_images=imgs[1:],
    save_all=True, duration=100, loop=0,transparency=255, disposal=2,optimize=False) 



#transparency=255, disposal=2,optimize=False) 

description="Version 1.0e | 26 april 2022 | Ping Snrasha for any feedback, idea or typo.\nD,U hotkey for load spritesheet.\nFor hero, will display the animation a bit much longer."
gifScaling=["1","2","3","4","5","6","7","8","9"]
      
class Application(ttk.Frame):
    def  __init__(self,window):
        ttk.Frame.__init__(self,window)

        style = ttk.Style(window)
        style.theme_use('clam')

        self.window=window
        self.pack(fill=tk.BOTH,expand=True)
        self.bg = style.lookup('TFrame', 'background')
        self.window.bind("<KeyRelease>", self.onKeyRelease)

        frame1=ttk.Frame(self,borderwidth=1,relief="sunken",padding=(5,5))
        frame1.pack(fill=tk.BOTH,side=tk.TOP,padx=(3,3),pady=(3,3))
        frame2=ttk.Frame(self)
        frame2.pack(fill=tk.BOTH,side=tk.LEFT,padx=(3,3),pady=(3,3))
        frame3=ttk.Frame(self)
        frame3.pack(fill=tk.BOTH,side=tk.RIGHT,padx=(3,3),pady=(3,3))
        self.checkBoxVar=[]
        self.checkBoxVar+=[tk.IntVar()]
        frame5=ttk.Frame(frame3)
        frame5.pack(fill=tk.BOTH,side=tk.TOP)
        checkbtn = tk.Checkbutton(frame5,text="Double background(V)", variable = self.checkBoxVar[0], onvalue = 1, offvalue = 0,bg=self.bg)
        checkbtn.pack(side=tk.LEFT)
        self.checkBoxVar+=[tk.IntVar()]
        checkbtn = tk.Checkbutton(frame5,text="Set canvas to 24x24(F)", variable = self.checkBoxVar[1], onvalue = 1, offvalue = 0,bg=self.bg)
        self.checkBoxVar[1].set(1)
        checkbtn.pack(side=tk.LEFT)
       
        
        button=ttk.Button(frame2,text="Unit(D)",command=self.onClickUnit)
        button.pack(fill=tk.BOTH,side=tk.TOP)
        button=ttk.Button(frame2,text="Hero(U)",command=self.onClickHero)
        button.pack(fill=tk.BOTH,side=tk.TOP)
        self.checkBoxVar+=[ tk.StringVar()]
        frame4=ttk.Frame(frame3)
        frame4.pack(fill=tk.BOTH,side=tk.TOP)
        
        label=ttk.Label(frame4,text="Scaling(+/-)")
        label.pack(fill=tk.BOTH,side=tk.RIGHT)        
        optionMenu=ttk.OptionMenu(frame4,self.checkBoxVar[2],gifScaling[5],*gifScaling)
        optionMenu.pack(fill=tk.BOTH,side=tk.RIGHT)

  
        label=ttk.Label(frame1,text=description)
        label.pack(fill=tk.BOTH,side=tk.TOP)

        self.window.bind('<Escape>', self.onClosing)


    
    def onClosing(self,event=None):
        self.window.destroy()
    def onClickHero(self):
        self.callGif(True)
    def onClickUnit(self):
        self.callGif(False)
        

    def callGif(self,isHero):
        filename=askFile()
        if(filename!=None):
            choice=[0,0,0,isHero]
            choice[0]=self.checkBoxVar[0].get()
            choice[1]=self.checkBoxVar[1].get()
            choice[2]=int(self.checkBoxVar[2].get() )
            toGif(filename,choice)
            return
    def onKeyRelease(self,event):
        if(event.char=='d'):
            self.onClickUnit()
        if(event.char=='u'):
            self.onClickHero()
        if(event.char=='f'):
            if( self.checkBoxVar[1].get()==1):
                self.checkBoxVar[1].set(0)
            else:
                self.checkBoxVar[1].set(1)
        if(event.char=='v'):
            if( self.checkBoxVar[0].get()==1):
                self.checkBoxVar[0].set(0)
            else:
                self.checkBoxVar[0].set(1)
        if(event.char=='+'):
            val=int(self.checkBoxVar[2].get())
            if(val>=len(gifScaling)):
                val=len(gifScaling)-1
            self.checkBoxVar[2].set(gifScaling[val])
        if(event.char=='-'):
            val=int(self.checkBoxVar[2].get())-2
            if(val<0):
                val=0
            self.checkBoxVar[2].set(gifScaling[val])


## Windows with the settings and title.
class Windows(tk.Tk):
    def __init__(self):
        
        super().__init__()
        # root window
        self.title("Hero's Hour Tool Animation")
        self.geometry("400x160+300+300")
        
        app=Application(self)
        self.protocol("WM_DELETE_WINDOW", app.onClosing)
        
if __name__ == '__main__':
    windows = Windows()
    windows.mainloop()



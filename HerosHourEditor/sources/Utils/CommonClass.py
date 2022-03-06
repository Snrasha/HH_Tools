import tkinter as tk
import tkinter.ttk as ttk
import Utils.CommonFunctions as CommonFunctions
## Label do not have set and get method. This class will do that.     
class LabelSimplified(ttk.Label):
    def __init__(self,master=None,**kwargs):
        self.var= tk.StringVar(master)
        ttk.Label.__init__(self,master,textvariable=self.var,**kwargs)
        self.get,self.set=self.var.get,self.var.set
class EntrySimplified(tk.Entry):
    def __init__(self,master=None,**kwargs):
        tk.Entry.__init__(self,master,**kwargs)
    def set(self,text):
        self.empty()
        if(text!=None):
            self.insert(0,text)
    def empty(self):
        self.delete(0, tk.END)
class FileFrame(ttk.LabelFrame):
    def __init__(self,parent=None,master=None,side=tk.TOP,anchor=None,fill=None,**kwargs):
        ttk.LabelFrame.__init__(self,parent,text='File', padding=(5, 5))
        if(master==None):
            master=parent
        self.master=master
        self.pack(side=side,anchor=anchor,padx=(1,1),pady=(1,1),fill=fill)
                
        editButton=ttk.Button(self,text='Edit (D)',command=self.master.editFile,width=12)
        editButton.pack(side=tk.LEFT,padx=5,pady=5)

        saveButton=ttk.Button(self,text='Save as (V)',command=self.master.saveFile,width=12)
        saveButton.pack(side=tk.LEFT,padx=5,pady=5)

class Field(ttk.Frame):
    def __init__(self,master,titleField,hintField="",side=tk.TOP,width=None,**kwargs):
        ttk.Frame.__init__(self,master)
        self.pack(fill=tk.BOTH,side=side,padx=(1,1),pady=(1,1))
                
        label=ttk.Label(self,text=titleField)
        if(width!=None):
            self.entry=tk.Entry(self, font='bold',width=width)
        else:
            self.entry=tk.Entry(self, font='bold')
        self.entry.pack(side=tk.RIGHT,padx=5)
        
        
        if(width!=None):
            s=tk.RIGHT
        else:
            s=tk.LEFT
            
        label.pack(side=s,padx=5,pady=5)

##        self.entry=tk.Text(self, font='bold',height=1,width=20)
##        self.entry.pack(side=tk.RIGHT,padx=5)
##        if(hintField!=None):
##            self.set(hintField)
##    def get(self):
##        return self.entry.get("1.0",tk.END)
##    def set(self,text):
##        self.empty()        
##        self.entry.insert("1.0",text)
##    def empty(self):
##        self.entry.delete("1.0", tk.END)

        if(hintField!=None):
            self.set(hintField)
    def get(self):
        return self.entry.get()
    def set(self,text):
        self.empty()
        if(text==None):
            return
        self.entry.insert(0,text)
    def empty(self):
        self.entry.delete(0, tk.END)
   
class FattyField(Field):
    def __init__(self,master,titleField,hintField="",side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField,hintField)
        self.entry.bind("<Button-1>",self.onEnter)
    def onEnter(self,event):
        self.entry.configure(state=tk.DISABLED)
        EntryPopup(self,event.x_root,event.y_root)

        
class FieldList(Field):
    def __init__(self,master,titleField,listOfItems,dictionnary=None,description="None",side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField)
        
        self.listOfItems=listOfItems
        self.dictionnary=dictionnary
        self.description=description

        self.entry.bind("<Button-1>",self.onEnter)
        
        for item in listOfItems:
            self.set(item)
            return
        
    def onEnter(self,event):
        self.entry.configure(state=tk.DISABLED)
        ListPopup(self,event.x_root,event.y_root)
        
    def getKeys(self):
        return self.listOfItems
    def getDict(self):
        return self.dictionnary
    def getDescription(self):
        return self.description
class FieldAdditiveList(Field):
    def __init__(self,master,titleField,description="None",side=tk.TOP,**kwargs):
        Field.__init__(self,master,titleField)
        self.description=description
        self.entry.bind("<Button-1>",self.onEnter)
        self.items=[]
        

    def onEnter(self,event):
        self.entry.configure(state=tk.DISABLED)
        AdditiveListPopup(self,event.x_root,event.y_root)
    def setItems(self,items):
        self.items=items
        for item in items:
            self.set(item)
            return
        
    def getItems(self):
        return self.items
    def getDescription(self):
        return self.description
class Tab(ttk.Frame):
    def  __init__(self,master,window,**kwargs):
        ttk.Frame.__init__(self,master,**kwargs)
        self.master=master
        self.window=window
    
    def onKeyRelease(self,event):
        None
    def bindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)
    def unBindKey(self):
        self.window.bind("<KeyRelease>", self.onKeyRelease)

class Popup(tk.Toplevel):
    def __init__(self,frame,x,y,width=200):
        tk.Toplevel.__init__(self,frame)
        style = ttk.Style(self)
        self.configure(background=style.lookup('TFrame', 'background'))

        self.title("Popup")
        self.geometry(str(width)+"x200+"+str(x-100)+"+"+str(y-100))
        self.focus()
        
        self.bind("<KeyPress>", self.onKeyDown)
        self.bind('<Escape>', self.onEscape)
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
    def onEscape(self,event=None):
        self.destroy()
    def onKeyDown(self,event):
        if(len(event.char)!=1):
            return
        if(ord(event.char)==13):
            self.destroy()
            
##class TextPopup(Popup):
##    def __init__(self,frame,x,y,text):
##        Popup.__init__(self,frame,x,y)
##        label=LabelSimplified(self)
##        label.set(text)
##        label.pack(side=tk.LEFT,padx=1,pady=1)
class EntryPopup(Popup):
    def __init__(self,field,x,y,width=600):
        Popup.__init__(self,field,x,y)
        self.field=field
        self.entry=tk.Text(self, font='bold')
        self.entry.delete('1.0', tk.END) 
        self.entry.insert('1.0',field.get())
        self.entry.pack(fill=tk.BOTH,side=tk.RIGHT,padx=5,expand=True)
        self.bind("<KeyPress>", self.onKeyDown)
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
        self.bind('<Escape>', self.onEscape)
    def onEscape(self,event=None):
        self.field.entry.configure(state=tk.NORMAL)
        self.field.set(self.entry.get("1.0",tk.END))
        self.destroy()
        
    def onKeyDown(self,event):
        if(len(event.char)!=1):
            return
        if(ord(event.char)==13):
            if(type(self.focus_get()) == tk.Text):
                return
            else:
                self.onEscape()
        
class ListPopup(Popup):
    def __init__(self,field,x,y):
        Popup.__init__(self,field,x,y,width=400)

        self.listbox = tk.Listbox(self)
        self.field=field
        
        self.listbox.delete(0, 'end')
        first=None
        for item in field.getKeys():
            if(first==None):
                first=item
            self.listbox.insert('end', item)
        self.bind("<KeyPress>", self.onKeyDown)
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
        self.bind('<Escape>', self.onEscape)

        self.listbox.bind('<Double-Button-1>', self.onDoubleClickListBox)
        self.listbox.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,expand=True)
        subframe1=ttk.LabelFrame(self,text='Description', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,expand=True,side=tk.TOP,padx=(1,1),pady=(1,1))

        self.labelDesc=ttk.Label(subframe1,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.LEFT,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)
        if(field.getDict()!=None):
            self.listbox.bind('<<ListboxSelect>>', self.onSelectListBox)
            self.labelDesc.configure(text=self.field.getDict()[first])
        else:
            self.labelDesc.configure(text=self.field.getDescription())

    def onEscape(self,event=None):
        self.field.entry.configure(state=tk.NORMAL)
        self.destroy()            
        
    def onDoubleClickListBox(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.field.entry.configure(state=tk.NORMAL)
        self.field.set(value)
        self.destroy()
        
    def onSelectListBox(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.labelDesc.configure(text=self.field.getDict()[value])

class AdditiveListPopup(Popup):
    def __init__(self,field,x,y):
        Popup.__init__(self,field,x,y,width=400)

        frame=ttk.Frame(self)
        frame.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,expand=True)
        self.entry=EntrySimplified(frame)
        self.entry.pack(side=tk.TOP)

        self.listbox = tk.Listbox(frame)
        self.field=field

        self.bind("<KeyPress>", self.onKeyDown)
        self.protocol("WM_DELETE_WINDOW", self.onEscape)
        self.bind('<Escape>', self.onEscape)
        self.bind('<Delete>', self.onDelete)

        self.listItems=field.getItems()
        

        self.listbox.delete(0, 'end')
        for item in self.listItems:
            self.listbox.insert('end', item)

        self.listbox.bind('<Double-Button-1>', self.onDoubleClickListBox)
        self.listbox.pack(side=tk.TOP,fill=tk.BOTH,padx=5,expand=True)
        subframe1=ttk.LabelFrame(self,text='Description', padding=(5, 5))
        subframe1.pack(fill=tk.BOTH,expand=True,side=tk.TOP,padx=(1,1),pady=(1,1))

        self.labelDesc=ttk.Label(subframe1,justify=tk.CENTER)
        self.labelDesc.pack(side=tk.LEFT,fill=tk.Y,expand=True,padx=5,pady=5)
        self.labelDesc.config(wraplength=200)

        self.labelDesc.configure(text=self.field.getDescription())


            
    def onEscape(self,event=None):
        self.field.entry.configure(state=tk.NORMAL)
        self.field.set(self.listbox.get(0))
        self.field.setItems(self.listItems)
        self.destroy()
    def onDelete(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        del self.listItems[index]
        self.listbox.delete(index)
        
        
    def onDoubleClickListBox(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
                
        self.entry.delete(0, tk.END)
        self.entry.insert(0,value)
        self.entry.focus()
        
        
        
    def onKeyDown(self,event):
        if(len(event.char)!=1):
            return
        # If the user is on an entry / input field, skip the event.
        if(CommonFunctions.checkIfInputField(type(self.focus_get()))):
            if(ord(event.char)==13):
                self.listbox.insert('end', self.entry.get().strip())
                self.listItems+=[self.entry.get().strip()]
                self.entry.delete(0, tk.END)
                
                self.focus()
            return
        

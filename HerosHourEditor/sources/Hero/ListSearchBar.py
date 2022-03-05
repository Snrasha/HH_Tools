import tkinter as tk
import tkinter.ttk as ttk

import Utils.CommonFunctions as CommonFunctions

## Init a search bar with a list box and all the events linked to it.
class SearchBar(ttk.Frame):

    def  __init__(self,master,parent):
        ttk.Frame.__init__(self,master,padding=(5,5))
        self.pack(fill=tk.BOTH,side=tk.LEFT)
        self.parent=parent
        self.descriptionsSkills=CommonFunctions.readSkills()
        self.skills=self.descriptionsSkills.keys()

        self.entry = tk.Entry(master,bd=2)
        self.entry.pack(side=tk.TOP,padx=5,pady=5)
        self.entry.bind('<KeyRelease>', self.readSearchBarAndReloadListBox)
        self.listbox = tk.Listbox(master,bd=2)

        self.listbox.bind('<<ListboxSelect>>', self.onSelectListBox)
        self.listbox.bind('<Double-Button-1>', self.onDoubleClickListBox)

        self.listbox.pack(side=tk.TOP,fill=tk.Y,padx=5,pady=5)
        self.update(self.skills)



    ## On double click of the list box, send the item clicked to the parent for fill a slot.
    def onDoubleClickListBox(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        
        self.parent.setValue(value)
        

    ## When you select a item on the list box, set the text of the description label.
    def onSelectListBox(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.parent.labelDesc.configure(text=self.descriptionsSkills[value])


    ## Get the value of the search bar and reduce the list bar to only descriptions or skills which is filling the word
    def readSearchBarAndReloadListBox(self,event):
            val = event.widget.get()
            if val == '':
                    data = self.skills
            else:
                    data = []
                    for item in self.skills:
                            if val.lower() in item.lower():
                                    data.append(item)
                            elif val.lower() in self.descriptionsSkills[item].lower():
                                data.append(item)
            self.update(data)


    ## Clear the list box and refill it with the data.
    def update(self,data):
            self.listbox.delete(0, 'end')
            for item in data:
                    self.listbox.insert('end', item)





import tkinter as tk


def readSkills():
    file1 = open("Skills.csv", 'r')
    lines=file1.readlines()
    skills=["None"]
    descriptionsSkills={"None":"Click on a skill on the list or the skill tree for get the description"}
    for line in lines:
        if(line.startswith('#')):
           continue
        split=line.split(";")
        skills+=[split[0]]
        descriptionsSkills[split[0]]=split[1]
        
    file1.close()

    return (skills,descriptionsSkills)

class SearchBar(tk.Frame):
    def  __init__(self,master,parent):
        tk.Frame.__init__(self,master,padx=5,pady=5)
        self.pack(fill=tk.BOTH,side=tk.LEFT)
        self.parent=parent
        self.skills,self.descriptionsSkills=readSkills()

        self.entry = tk.Entry(master)
        self.entry.pack(side=tk.TOP,padx=5,pady=5)
        self.entry.bind('<KeyRelease>', self.scankey)
        self.listbox = tk.Listbox(master)
##        self.listbox.bind('<<ListboxSelect>>', self.descriptionSkillKey)

        self.listbox.bind('<<ListboxSelect>>', self.descriptionSkillKey)
        self.listbox.bind('<Double-Button-1>', self.printValue)

        self.listbox.pack(side=tk.TOP,fill=tk.Y,padx=5,pady=5)
        self.update(self.skills)

    def printValue(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print ('You selected item '+value)
        if(self.parent.currentHover!=None):
            self.parent.setValue(value)
            

        return
        

    def descriptionSkillKey(self,event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
##        print ('You selected item %d: "%s"' % (index, value))
        self.parent.labelDesc.configure(text=self.descriptionsSkills[value])
    def scankey(self,event):
            val = event.widget.get()
##            print(val)
            if val == '':
                    data = self.skills
            else:
                    data = []
                    for item in self.skills:
                            if val.lower() in item.lower():
                                    data.append(item)				  
            self.update(data)


    def update(self,data):
            

            self.listbox.delete(0, 'end')

            # put new data
            for item in data:
                    self.listbox.insert('end', item)





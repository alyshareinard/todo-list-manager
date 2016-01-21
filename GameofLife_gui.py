try:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk
    from tkinter.messagebox import *

except ImportError:
    import Tkinter as tk
    import Tkinter.font as tkFont
    import Tkinter.ttk as ttk
    from tkMessageBox import *
import sys
import time
from datetime import date
from datetime import timedelta
import datetime
from math import *
import os
#from button import *
import pickle
from array import array



#    def add_challenge(self, name=None, pt_val=None, notes=None, context=None, realm=None,\
 #                     subrealm=None, repeat=None, repeat_time=None, repeat_reset=None,\
  #                    isboss=None, boss=None, unlocked_by=None, date_last_comp=[],\
   #                   next_active=None, due_date="", active="Y", planned_date="", completed='N'):








class popupwindow(object):
    def __init__(self, master, name=None, pt_val=5, realm="work", context=None, duedate=None, repeat=None, repeat_time=None):
       
        top=self.top=tk.Toplevel(master)
#        top.geometry('300x600')
        row_val=0        
        self.l=ttk.Label(top,text="Add task information").grid(column=0, row=row_val)#, sticky=(N, W, E, S))
        self.name=tk.StringVar()

        row_val+=1
        name_label=ttk.Label(top, text="Name: ").grid(column=0, row=row_val)
        name_entry=ttk.Entry(top, textvariable=self.name).grid(column=1, row=row_val)
        if name!=None:
            self.name.set(name)
#        print("adding name: ", self.name)

        
        row_val+=1
        pt_val_label=ttk.Label(top, text="Point value: ").grid(column=0, row=row_val)
        self.pts=tk.StringVar()
        pt_val_entry=ttk.Entry(top, textvariable=self.pts).grid(column=1, row=row_val)
        
        self.pts.set(pt_val)

        row_val+=1
        #TODO need to make this configurable -- global variable?
        realms={"home", "well-being", "health", "work"}
        realm_label=ttk.Label(top, text="Realm: ").grid(column=0, row=row_val)
        self.realm=tk.StringVar(master)
        realm_menu=ttk.OptionMenu(top, self.realm, *realms)
        if realm!=None:
            self.realm.set(realm)
        else:
            self.realm.set("work")
            
        realm_menu.grid(column=1, row=row_val)

        row_val+=1
        context_label=ttk.Label(top, text="Context: ").grid(column=0, row=row_val)
        self.context=tk.StringVar()
        context_entry=ttk.Entry(top, textvariable=self.context).grid(column=1, row=row_val)
        if context!=None:
            self.context.set(context)

        row_val+=1
        due_label=ttk.Label(top, text="Due date: ").grid(column=0, row=row_val)
        self.due=tk.StringVar()
        due_entry=ttk.Entry(top, textvariable=self.due).grid(column=1, row=row_val)        

        row_val+=1
        rpt={"no", "yes"}
        repeat_label=ttk.Label(top, text="Repeat: ").grid(column=0, row=row_val)
        self.repeat=tk.StringVar(master)
        repeat_menu=ttk.OptionMenu(top, self.repeat, *rpt)
        if repeat!=None:
            self.repeat.set(repeat)
        else:
            self.repeat.set("no")
        repeat_menu.grid(column=1, row=row_val)

        row_val+=1    
        rpt_time_label=ttk.Label(top, text="Repeat time (days): ").grid(column=0, row=row_val)
        self.repeat_time=tk.StringVar(master)
        rpt_time_entry=ttk.Entry(top, textvariable=self.repeat_time).grid(column=1, row=row_val)
        if repeat_time!=None:
            self.repeat_time.set(repeat_time)
        
        row_val+=1
        self.b=ttk.Button(top,text='Ok',command=self.cleanup)
        self.b.grid(column=0, row=row_val)


            
    def cleanup(self):
        me.add_challenge_basic(name=self.name.get(), pt_val=self.pts.get(), realm=self.realm.get(), context=self.context.get(), due_date=self.due.get(), repeat=self.repeat.get(), repeat_time=self.repeat_time.get())
        print("repeat? ", self.repeat.get())
        if self.repeat.get()=="yes":
            askyesno("Habit?", "Add this to the habit bank?")
            me.add_habit(name=self.name.get(), pt_val=self.pts.get(), realm=self.realm.get(), context=self.context.get(), repeat_time=self.repeat_time.get())
        self.top.destroy()        

        
class habitwindow(object):
    def __init__(self, master):
        self.tree = None
        self.master=master
        top=self.top=tk.Toplevel(master)
        top.title("Habit bank")
        self.container=container = ttk.Frame(self.top, width=100, height=10)
        container.pack(fill='both', expand=True)
        temp=ttk.Label(container, text="what's up!?")
        #this should just display all the habits so far
        self._setup_widgets()
        self._build_tree()


    def _setup_widgets(self):
#        s = """click on header to sort by that column
#to change width of column drag boundary
#        """
        msg = ttk.Label(self.top, wraplength="4i", justify="left", anchor="n",
            padding=(2, 2, 2, 6), text="Click to add habit to todo list, Ok to finish")
        msg.pack(fill='x')



        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(self.top, columns=habit_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)

##TODO THE FOLLOWING LINES CAUSE TROUBLE BUT SHOULD BE ADDED BACK IN!
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.pack()
        self.b=ttk.Button(self.top,text='Ok',command=self.cleanup)
        self.b.pack()
##        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.top)
##        vsb.grid(column=1, row=0, sticky='ns', in_=container)
##        hsb.grid(column=0, row=1, sticky='ew', in_=container)
##        container.grid_columnconfigure(0, weight=1)
##        container.grid_rowconfigure(0, weight=1)


    def _build_tree(self):

        for col in habit_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for task_item in me.habitlist:
            print("in habit list loop")
            item=[]
            print(task_item.uniq_id)
            print(habit_header)
            print(task_item)
            #make this into a list that the following can understand
            for col_val in habit_header:
                
                if col_val == "Habit #":
                    item.append(str(task_item.uniq_id))
                    print(task_item.uniq_id)
                    print(item)
#                    item.append(tk.Checkbutton(self, command=me.toggle_completed(task_item.uniq_id)))
                if col_val == "name":
                    item.append(str(task_item.name))
                if col_val == "realm":
                    item.append(str(task_item.realm))
                if col_val == "context":
                    item.append(str(task_item.context))
                if col_val == "points":
                    item.append(str(task_item.pt_val))

                
            self.tree.insert('', 'end', values=item, tags=(task_item.uniq_id))
            self.tree.tag_bind(task_item.uniq_id, '<<TreeviewSelect>>', self.addhabit)
            count=0
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
#                    print("ix, val", ix, val)
                    
#                    print("count", count)
                count=count+1
                col_w = tkFont.Font().measure(val)
                if self.tree.column(habit_header[ix],width=None)<col_w:
                    self.tree.column(habit_header[ix], width=col_w)


    def addhabit(self, event):

        item_id = str(self.tree.focus())

        item=self.tree.item(item_id)
        values=item['values']
        uid=item['tags']
        uid=uid[0]

        newhabit=me.habitlist[uid]
        
        
        self.w=popupwindow(self.master, name=newhabit.name, pt_val=newhabit.pt_val, realm=newhabit.realm, context=newhabit.context, repeat="yes", repeat_time=newhabit.repeat_time)
        self.master.wait_window(self.w.top)


##        #grab the task that was just added to challenge list and put it in the display -- Commented out because it's adding the new task (created from the habit bank) to the habit bank
##        task_item=me.challengelist[-1]
###        for task_item in me.challengelist:
##            
###            print(task_item)
##        item=[]    
##        for col_val in view_header:
##            if col_val == "Task #":
##                item.append(str(task_item.uniq_id))
##            if col_val == "name":
##                item.append(str(task_item.name))
##            if col_val == "realm":
##                item.append(str(task_item.realm))
##            if col_val == "context":
##                item.append(str(task_item.context))
##            if col_val == "points":
##                item.append(str(task_item.pt_val))
##            if col_val == "due date":
##                item.append(str(task_item.due_date))
##            
##        self.tree.insert('', 'end', values=item, tags=(task_item.uniq_id, "uncompleted"))


    def cleanup(self):
##        if self.habit=="yes":
##            me.add_habit(name=self.name.get(), pt_val=self.pts.get(), realm=self.realm.get(), context=self.context.get(), due_date=self.due.get(), repeat=self.repeat.get())
        self.top.destroy() 
        
class MultiColumnListbox(tk.Frame):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, master):
        super(MultiColumnListbox, self).__init__()
        self.tree = None
        self.master=master
        self.no_completed=True
        self._setup_widgets()
        self._build_tree()


    def _setup_widgets(self):
#        s = """click on header to sort by that column
#to change width of column drag boundary
#        """
#        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
#            padding=(10, 2, 10, 6), text=s)
#        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=view_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        add_button=ttk.Button(self.master, text="Add task", command=self.add_popup)
        add_button.pack(side=tk.LEFT)
        habit_button=ttk.Button(self.master, text="Add habit", command=self.habit_popup)
        habit_button.pack(side=tk.LEFT)
        remove_button=ttk.Button(self.master, text="Remove completed", command=self.remove_completed)
        remove_button.pack(pady=20, padx=20, side=tk.RIGHT)

    def remove_completed(self):
        for item_id in self.tree.get_children():
            tree_val=self.tree.item(item_id)
            if "completed" in tree_val["tags"]:
                self.tree.delete(item_id)

    def add_popup(self):
        self.w=popupwindow(self.master)
        self.master.wait_window(self.w.top)

        #grab the task that was just added to challenge list and put it in the display
        task_item=me.challengelist[-1]
#        for task_item in me.challengelist:
            
#            print(task_item)
        item=[]    
        for col_val in view_header:
            if col_val == "Task #":
                item.append(str(task_item.uniq_id))
            if col_val == "name":
                item.append(str(task_item.name))
            if col_val == "realm":
                item.append(str(task_item.realm))
            if col_val == "context":
                item.append(str(task_item.context))
            if col_val == "points":
                item.append(str(task_item.pt_val))
            if col_val == "due date":
                item.append(str(task_item.due_date))
            
        self.tree.insert('', 'end', values=item, tags=(task_item.uniq_id, "uncompleted"))

    def habit_popup(self):
        #habitwindow is a popup that displays habits
        self.h=habitwindow(self.master)
        self.master.wait_window(self.h.top)

        #grab the task that was just added to challenge list and put it in the display
        task_item=me.challengelist[-1]

        item=[]    
        for col_val in view_header:
            if col_val == "Task #":
                item.append(str(task_item.uniq_id))
            if col_val == "name":
                item.append(str(task_item.name))
            if col_val == "realm":
                item.append(str(task_item.realm))
            if col_val == "context":
                item.append(str(task_item.context))
            if col_val == "points":
                item.append(str(task_item.pt_val))
            if col_val == "due date":
                item.append(str(task_item.due_date))
            
        self.tree.insert('', 'end', values=item, tags=(task_item.uniq_id, "uncompleted"))        

    def entryValue(self):
        print(self.w.realm)
        print(self.w.name)
        
    def onClick(self, event):

        item_id = str(self.tree.focus())

        item=self.tree.item(item_id)

        uid=item['tags']
        uid=uid[0]
        completed=0
        completed=me.toggle_completed(uid)


        if completed=="Y":
            temp_val=item['values']
            temp_tags=item['tags']
            type(temp_val)
            self.tree.delete(item_id)
            self.tree.insert('', 'end', values=temp_val, tags=(temp_tags[0], "completed"))
        if completed=="N":
            temp_val=item['values']
            temp_tags=item['tags']
            type(temp_val)
            self.tree.delete(item_id)
            self.tree.insert('', 'end', values=temp_val, tags=(temp_tags[0], "uncompleted"))            

    
    def _build_tree(self):
        for col in view_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for task_item in me.challengelist:
            #skip completed challenges if no_completed is True
            if not (self.no_completed==True and task_item.completed=="Y"):
                item=[]
#                print(task_item.uniq_id)
#                print(view_header)
                #make this into a list that the following can understand
                for col_val in view_header:
                    
                    if col_val == "Task #":
                        item.append(str(task_item.uniq_id))
#                        print(task_item.uniq_id)
#                        print(item)
#                    item.append(tk.Checkbutton(self, command=me.toggle_completed(task_item.uniq_id)))
                    if col_val == "name":
                        item.append(str(task_item.name))
                    if col_val == "realm":
                        item.append(str(task_item.realm))
                    if col_val == "context":
                        item.append(str(task_item.context))
                    if col_val == "points":
                        item.append(str(task_item.pt_val))
                    if col_val == "due date":
                        item.append(str(task_item.due_date))
                    
                self.tree.tag_configure("completed", background='orange')
                if task_item.completed=='Y': comp_val="completed"
                if task_item.completed=='N': comp_val="uncompleted"
                
                self.tree.insert('', 'end', values=item, tags=(task_item.uniq_id, comp_val))
                self.tree.tag_bind(task_item.uniq_id, '<<TreeviewSelect>>', self.onClick)
                count=0
                # adjust column's width if necessary to fit each value
                for ix, val in enumerate(item):
#                    print("ix, val", ix, val)
                        
#                    print("count", count)
                    count=count+1
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(view_header[ix],width=None)<col_w:
                        self.tree.column(view_header[ix], width=col_w)

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))




class avatar:
    def __init__(self):
        #search current directory for save file
        directory=os.getcwd()
        print(directory)
        if os.path.isfile(directory+"/Life_challenge_file.txt") and os.path.isfile(directory+"/Life_points_file.txt") and os.path.isfile(directory+"/Life_preferences.txt" and os.path.isfile(directory+"/Life_habit_file.txt")):
            f=open(directory+'/Life_challenge_file.txt', mode='rb')
            self.challengelist=pickle.load(f)
            f.close()
            
            f=open(directory+'/Life_points_file.txt', mode='rb')
            self.record=pickle.load(f)
            f.close()
            
            f=open(directory+'/Life_preferences.txt', mode='rb')
            self.prefs=pickle.load(f)
            f.close()
            
            f=open(directory+"/Life_habit_file.txt", 'wb')
            self.habitlist=pickle.load(f)
            f.close()
        elif os.path.isfile(directory+"/Life_challenge_file.txt"):
            f=open(directory+'/Life_challenge_file.txt', mode='rb')
            self.challengelist=pickle.load(f)
            f.close()
            
            num_realms=4
            num_subrealms=[2,6,2,2]
            realm_names=["home", "work", "health", "well-being"]
            ideal_pts=[20, 60, 20, 20]
            self.prefs=prefs(num_realms, num_subrealms, realm_names, ideal_pts)            

            today=datetime.datetime.combine(date.today(), datetime.time(0, 0)) 
            self.record=points(today, [0, 0, 0, 0])

            if os.path.isfile(directory+"/Life_habit file.txt"):
                f=open(directory+"/Life_habit_file.txt", 'wb')
                pickle.dump(self.habitlist, f)
                f.close()
            else:
                self.habitlist=[]
                self.add_habit(name="eat fruit", realm="health", pt_val=1, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)), repeat="Y", repeat_time=1)
                self.add_habit(name="eat grains", realm="health",  pt_val=1, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)), repeat="Y", repeat_time=1)
            self.save_challenges()
        
        else:
        #if no file then initialize object
            self.avatar_initial_setup()



    def avatar_initial_setup(self):
        directory=os.getcwd()
#        print(directory)

        if os.path.isfile(directory+"/Life_preferences.txt"):
            f=open(directory+"/Life_preferences.txt", mode='rb')
            pickle.load(f)
            f.close()
        else:
            num_realms=4
            num_subrealms=[2,6,2,2]
            realm_names=["home", "work", "health", "well-being"]
#            self.level=0
#            self.points=0
            ideal_pts=[20, 60, 20, 20]
            self.prefs=prefs(num_realms, num_subrealms, realm_names, ideal_pts)
                    
        today=datetime.datetime.combine(date.today(), datetime.time(0, 0)) 
        self.record=points(today, [0, 0, 0, 0])
        
        self.challengelist=[]


        if os.path.isfile(directory+"/Life_habit file.txt"):
            f=open(directory+"/Life_habit_file.txt", 'wb')
            pickle.load(f)
            f.close()
        else:
            self.habitlist=[]
            self.add_habit(name="eat fruit", realm="health", pt_val=1, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)), repeat="Y")
            self.add_habit(name="eat grains", realm="health",  pt_val=1, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)), repeat="Y")

        self.add_challenge_basic(name="finish program edits", realm="well-being", pt_val=1, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)))
        self.add_challenge_basic(name="relax", realm="well-being",  pt_val=1, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)))

##        f=open(directory+"/Life_challenge_file.txt", 'wb')
##        pickle.dump(self.challengelist, f)
##        f.close()
##        
##        f=open(directory+"/Life_preferences.txt", 'wb')
##        pickle.dump(self.prefs, f)
##        f.close()
##
###        print("Here's what it looks like now", self.record.date, self.record.realm_pts)
##        f=open(directory+"/Life_points_file.txt", 'wb')
##        pickle.dump(self.record, f)
##        f.close()

        self.save_challenges()

    def wrapper(self):
        option=""
        while option !='Q':
            option=input('\nOptions:\nA: add challenges\nC: complete challenges\nD: delete challenges\nP: plan or print\nQ: quit\n')
        
            if option=="A":
                option2=input('A: add single\nAM: add multiple\nAC:add completed\nAS: add sub\n')
                if option2=='A':
                    self.add_challenge()
                if option2=='AM':
                    self.add_challenges()
                if option2=='AC':
                    self.add_competed_challenge()
                if option2=='AS':
                    self.add_subchallenge()

            elif option=="C":
                option2=input("CM: complete multiple\nCR: complete on different day\nCRM: complete multiple on different day\n(Or just enter challenge number)\n")
                if option2.isdigit():
                    self.complete(int(option2))
                if option2=="CM":
                    num="-1"
                    while num !="-1":
                        num=input("challenge number: (-1 to stop)")
                        if int(num) > -1:
                            self.complete(int(num))
                if option2=="CR":
                    self.retro_complete()
                if option2=="CRM":
                    self.retro_comp_multiple()
                     
            elif option=='D':
                uniq_id=input("which challenge: ")
                self.delete_challenge(int(uniq_id))

            elif option=='P':
                option2=input("PW: print week\nPA: print active\nPR: print realm\nPC: print context\nPS: print sorted\nPB: print bosses\nPNW: plan next week\n")
                if option2=="PW":
                    self.print_week()
                if option2=="PA":
                    self.print_active()
                if option2=="PC":
                    context=input("which context: ")
                    self.print_challenges(context=context)
                if option2=="PB":
                    self.print_bosses()
                if option2=="PR":
                    realm=input("which realm: ")
                    self.print_challenges(realm=realm)
                if option2=="PS":
                    self.print_sorted()
                if option2=="PNW":
                    self.plan_next_week()

            elif option=='Q':
                return



##    def make_gui(self):
##        root=Tk()
##        root.title("The Game of Life")
##        root.geometry("800x400")
##        app=Application(root)
##        current_realm="work"
###        menubar=Menu(root)
##        def change_realm():
##            print("value is", realm_menu.get())
##            current_realm=realm_menu.get()
##            
##        def about():
##            print("routine created by Alysha Reinard to improve productivity")
##        def helpmenu():
##            print("TBD")
##
###        realm_menu=Menu(menubar, tearoff=0)
###        realm_menu.add_command(label="work", command=change_realm)
###        realm_menu.add_command(label="home", command=change_realm)
###        realm_menu.add_command(label="well-being", command=change_realm)
###        realm_menu.add_command(label="health", command=change_realm)
###        realm_menu.add_command(label="all", command=change_realm)
##                              
###        menubar.add_cascade(label="Realm", menu=realm_menu)
##        
##        k=0
##        for i in range(8):
##            while self.challengelist[k].realm!=current_realm or self.challengelist[k].active!='Y':
##                k=k+1
##            task=self.challengelist[k].short_print
##            k=k+1
##            print(k)
##            var = IntVar()
##            tasks = Checkbutton(root, text=str(self.challengelist[k].short_print), variable=str(self.challengelist[k].completed))
##
###        helpmenu = Menu(menubar, tearoff=0)
###        helpmenu.add_command(label="About", command=about)
###        menubar.add_cascade(label="Help", menu=helpmenu)
###        root.config(menu=menubar)
##        root.mainloop()


        
    def add_completed_challenge(self):
        self.add_challenge(completed='Y', active='N')


    def plan_next_week(self, realm="work"):
        self.print_overdue()
        print("active challenges (not daily, not currently planned)")
        length=range(len(self.challengelist))
#        self.print_todos(realm)
        print("\nDue dates in the next two weeks")
        self.print_due(14, realm)
        print("\nPlanned activities in the next two weeks")
        self.print_todo(14, realm)
        one_day=timedelta(days=1)
        day=datetime.datetime.combine(date.today(), datetime.time(0, 0)) 

        count=range(8)
        daysofweek=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for j in count:
            print("\n")
            dow=day.weekday()
            print("Unassigned tasks:")
            for i in length:
                if self.challengelist[i].planned_date==None and self.challengelist[i].completed=="N" and \
                   self.challengelist[i].realm==realm and self.challengelist[i].repeat=="N":
                    if self.challengelist[i].isboss=="Y":
                        print("BOSS ")#, end="")
                    if self.challengelist[i].active=="N" and self.challengelist[i].isboss=="N":
                        print("(")#, end="")
                    print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())#, end="")
                    if self.challengelist[i].active=="N" and self.challengelist[i].isboss=="N":
                        print(")")
                    else:
                        print("")
            print("\nPlanned for ", daysofweek[dow], day)
            self.print_todotoday(day=day)
            print("\n")

            task=1
            while task !="0":

                print("Day: ", daysofweek[dow], day)
                task=input("What task would you like to add (enter task #, 0 to move on, 'new' to add new challenge): ")
                if type(task) == str and task == "new":
                    self.add_challenge(planned_date=datetime.datetime.combine(day,datetime.time(0, 0)))
                elif task !="0" and task !="":
                    day=datetime.datetime.combine(day,datetime.time(0, 0)) 
                    self.change_tododate(int(task), day) 
            day=day+one_day
        self.save_challenges()

    def bib(self, uniq_id, days=1):
        """bump it back a day"""
        index=self.uniq2index(uniq_id)
        one_day=timedelta(days=days)
        if self.challengelist[index].planned_date != "None":
            self.challengelist[index].planned_date=self.challengelist[index].planned_date+one_day
            
    def print_week(self, realm="work"):
        self.print_overdue()
        print("\nUpcoming due dates")
        self.print_due(7,realm)
        print("\nTODO list")
        self.print_todo(7, realm)


    def delete_challenge(self, uniq_id):
        num=self.uniq2index(uniq_id)
        print("Deleting challenge ", self.challengelist[num].name)
        sure=input("Y/N?")
        if sure=="Y":
            self.challengelist.pop(num)
            print("deleted")
            length=range(len(self.challengelist))
            for i in length:
                if self.challengelist[i].unlocked_by !="" and self.challengelist[i].unlocked_by!=[]:
                    for uniq_id in self.challengelist[i].unlocked_by:
                        self.challengelist[i].unlocked_by.remove(uniq_id)
#

    def uncomplete(self, uniq_id):
        num=self.uniq2index(uniq_id)
        if self.challengelist[num].completed=="N":
            print("this challenge has not yet been completed ")
            return
        self.challengelist[num].completed='N'
        self.challengelist[num].active='Y'
        if self.challengelist[num].pt_val=="var":
            pt_val=float(input("What is the point value: "))
        else:
            pt_val=self.challengelist[num].pt_val
        date_cnt=-1
        for it in self.record.date:
            date_cnt+=1
            if it==datetime.datetime.date(self.challengelist[num].date_completed):
                realm_cnt=-1
                for name in self.prefs.realm_names:
                    realm_cnt+=1
                    if self.challengelist[num].realm==name:
                        self.record.realm_pts[date_cnt][realm_cnt]=self.record.realm_pts[date_cnt][realm_cnt]-float(pt_val)
                        print(self.record.date[date_cnt])
                        print(self.prefs.realm_names[0], self.record.realm_pts[date_cnt][0])
                        print(self.prefs.realm_names[1], self.record.realm_pts[date_cnt][1])
                        print(self.prefs.realm_names[2], self.record.realm_pts[date_cnt][2])
                        print(self.prefs.realm_names[3], self.record.realm_pts[date_cnt][3])
        self.challengelist[num].date_completed=None


    def update_pts(self, realm, date, pt_val):
        found=0
        date_cnt=-1
#        print("adding pt val: ", pt_val)
#        if type(date) == datetime.datetime:
#            date=date.date()
        print(self.record.date)
        print(date_cnt)
        for it in self.record.date:
            date_cnt=date_cnt+1
            print(date_cnt)
            print(it.date())
            print(date.date())
            if it.date()==date.date():
                print("in the loop")
                realm_cnt=-1
                for name in self.prefs.realm_names:
                    realm_cnt=realm_cnt+1
                    if realm==name:
#                        print(self.record.realm_pts[date_cnt][realm_cnt])
                        self.record.realm_pts[date_cnt][realm_cnt]=self.record.realm_pts[date_cnt][realm_cnt]+pt_val                        
                found=1
        print("found", found)
        if found==0: #today's date isn't found in points, so make a new column for today
            self.record.date.append(date.today())
            self.record.realm_pts.append([0,0,0,0])
            realm_cnt=-1
            date_cnt=date_cnt+1 #just move to the next one
            print(date_cnt)
            for name in self.prefs.realm_names:
                realm_cnt=realm_cnt+1
                if realm==name:
                    print(self.record.realm_pts)
                    print(date_cnt)
                    print(realm_cnt)
                    print(pt_val)
                    self.record.realm_pts[date_cnt][realm_cnt]=self.record.realm_pts[date_cnt][realm_cnt]+float(pt_val)


#        print(self.record.date[date_cnt])
#        print(self.prefs.realm_names[0], self.record.realm_pts[date_cnt][0])
#        print(self.prefs.realm_names[1], self.record.realm_pts[date_cnt][1])
#        print(self.prefs.realm_names[2], self.record.realm_pts[date_cnt][2])
#        print(self.prefs.realm_names[3], self.record.realm_pts[date_cnt][3])


    def uniq2index(self, uniq_id):       
        length=range(len(self.challengelist))
#        print("looking for: ", uniq_id)
        num=[]
        if type(uniq_id=='str'):
            uniq_id=int(uniq_id)
        for i in length:
            if self.challengelist[i].uniq_id == uniq_id:
                num.append(i)
        if len(num) >1:
            print("more than one challenge match that number")
            return
        if len(num)==0:
            print("no challenge found ", uniq_id)
            return
        return int(num[0])

    
    def complete(self, uniq_id, date_completed=datetime.datetime.combine(date.today(), datetime.time(0, 0))):

        num=int(self.uniq2index(int(uniq_id)))
        
        if self.challengelist[num].completed=="Y":
            print("this challenge has already been completed! ")
            return
        print("Congratulations on completing ", self.challengelist[num].name)
        self.challengelist[num].completed='Y'
        self.challengelist[num].active='N'
        self.challengelist[num].date_completed=date_completed
        if self.challengelist[num].pt_val=="var":
            pt_val=float(input("What is the point value: "))
        else:
            pt_val=float(self.challengelist[num].pt_val)
#            print("pt_val before update pts: ", pt_val)
#        comments=input("Any comments? ")
        if self.challengelist[num].repeat=='N' and comments != "":
            self.challengelist[num].comments.append(comments)
        self.update_pts(self.challengelist[num].realm, date_completed, pt_val)
        self.refresh_challenges()

        if self.challengelist[num].repeat=='Y':
            me.chain_length(self.challengelist[num].name, num)
            self.challengelist[num].completed="N"
            repeat_time=timedelta(days=self.challengelist[num].repeat_time)
            if self.challengelist[num].repeat_reset==0: #i.e. this resets from time last one appeared
                next_active=self.challengelist[num].date_created+repeat_time
            if self.challengelist[num].repeat_reset==1:
                next_active=datetime.datetime.combine(date.today()+repeat_time, datetime.time(0, 0))
            if not hasattr(me.challengelist[num], 'notes'):
                self.challengelist[num].notes=[]
            if self.challengelist[num].comments==None:
                self.challengelist[num].comments=[]
            elif type(self.challengelist[num].comments) != list:
                self.challengelist[num].comments=[self.challengelist[num].comments]
            if comments != "":
                self.challengelist[num].comments.append(comments)
            

            if self.challengelist[num].date_completed==None:
                old_completed=[]
                print("None")
            elif type(self.challengelist[num].date_completed)!=list:
                old_completed=[self.challengelist[num].date_completed]
                print("not list")
            else:
                old_completed=self.challengelist[num].date_completed
                print("list")

            old_completed.append(date_completed)
            self.challengelist[num].date_completed=old_completed

            self.challengelist[num].next_active=next_active
            self.challengelist[num].active="N"
#            self.add_challenge(name=self.challengelist[num].name, \
#                               context=self.challengelist[num].context, \
#                               pt_val=self.challengelist[num].pt_val,\
#                               realm=self.challengelist[num].realm, \
#                               subrealm=self.challengelist[num].subrealm, \
#                               repeat=self.challengelist[num].repeat, \
#                               repeat_time=self.challengelist[num].repeat_time, \
#                               repeat_reset=self.challengelist[num].repeat_reset, \
#                               isboss=self.challengelist[num].isboss, \
#                               boss=self.challengelist[num].boss, \
#                               date_last_comp=date_completed , \
#                               active="N",\
#                               notes="",\
#                               unlocked_by=[],\
#                               due_date=None,\
#                               planned_date=None,\
#                               next_active=next_active)

        self.save_challenges()


    def retro_complete(self, uniq_id=0, date_comp=None):
        """Add a completed challenge on a previous day"""
        if date_comp==None:
            date_comp=me.get_date()
        if uniq_id==0:
            uniq_id=input("which challenge? ")
        me.complete(uniq_id, date_comp)

    def retro_comp_multiple(self):
        date_comp=me.get_date()
        uniq_id=input("which challenge? ")
        while uniq_id != 'q':
            me.complete(uniq_id, date_comp)            
            uniq_id=input("which challenge (q to quit)? ")

    def print_pts(self, dd=7):
        today=date.today()
        one_week=timedelta(days=dd)
        length=range(len(self.record.date))
        totals=[]
        for i in range(self.prefs.num_realms):
            totals.append(0.0)
        for i in length:
            if self.record.date[i]>today-one_week:
                print(self.record.date[i], self.record.realm_pts[i])
                for j in range(self.prefs.num_realms):
                    totals[j]=totals[j]+self.record.realm_pts[i][j]
#                    print("total now: ", totals[j])
                                       
        print("Totals")
        for i in range(self.prefs.num_realms):
            print(self.prefs.realm_names[i]+": "+str(totals[i]))
        print("Percentages vs ideal: ")
        for i in range(self.prefs.num_realms):
            print(self.prefs.realm_names[i]+": "+str(int(100*totals[i]/self.prefs.ideal_pts[i]))+"%")
 

        
    def print_repeating(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].active=="Y" and self.challengelist[i].repeat=="Y":
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())

                
    def print_weekly(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].active=="Y" and self.challengelist[i].repeat=="Y" and self.challengelist[i].repeat_time==7:
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())

                

    def print_daily(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].active=="Y" and self.challengelist[i].repeat=="Y" and self.challengelist[i].repeat_time==1:
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())


    def print_threegoodthings(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].name=="three good things":
                print(self.challengelist[i].date_completed, self.challengelist[i].comments)

    def chain_length(self, challenge, last, printit=0):
        length=range(len(self.challengelist))
        count=0
        dates=[]
        #first run through all the challenges and look for others with the same name, count them and make
        #file called "dates" that holds all the dates
        for i in length:
            if self.challengelist[i].name==challenge and self.challengelist[i].completed=="Y":
                count=count+1
                if printit == 1:
                    print(self.challengelist[i].date_completed)
                dates.append(self.challengelist[i].date_completed)
        length=range(count-1, 0, -1)
        one_day=timedelta(days=self.challengelist[last].repeat_time)
        old_date=dates[count-1]
        count2=1
        #now count backwards through the dates you've collected and see how long they are sequential (i.e. to see
        #how many days in a row the challenge has been done).  
        for i in length:
            if dates[i]== old_date-one_day:
                count2=count2+1
                old_date=dates[i]
            else:
                i=0
        if count2 == 7:
            print("You're on a streak! 7 in a row!!")
        if count2 == 21:
            print ("I think you've got it. 21 in a row!  You advance to the next level on this challenge.")
            self.challengelist[last].repeat_time=2*self.challengelist[last].repeat_time
        print("You've done "+challenge+" " +str(count)+" days total and "+str(count2)+" days in a row")

                
    def print_active(self):
        length=range(len(self.challengelist))
        count=0
        for i in length:
            if self.challengelist[i].active=="Y":
                count=count+1
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
        print(str(count)+" active challenges")


    def print_sorted(self):
        length=range(len(self.challengelist))
        count=0
        for j in self.prefs.realm_names:
            print("\nRealm: ", j)
            for i in length:
                if self.challengelist[i].active=="Y" and self.challengelist[i].realm==j:
                    count=count+1
                    print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
        #run through one more time to find challenges that aren't labeled correctly
        for i in length:
            found=0
            for j in self.prefs.realm_names:
                if self.challengelist[i].active=="Y" and self.challengelist[i].realm==j:
                    found=1
            if self.challengelist[i].active=="Y" and found==0:
                print("!!! Missing appropriate realm")
                print(i, self.challengelist[i].long_print())
                count=count+1
        print("\n"+str(count)+" active challenges")

    def print_work(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].realm=="work":
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())



    def print_due(self, numdays, realm):
        due=[]
        length=range(len(self.challengelist))
        diff=timedelta(days=numdays)
        for i in length:
            if self.challengelist[i].due_date != None:
#                print(i)
                due_date=datetime.datetime.combine(self.challengelist[i].due_date, datetime.time(0, 0))

                today=datetime.datetime.combine(date.today(),datetime.time(0, 0)) 
                if due_date<=today+diff and self.challengelist[i].active=="Y" and self.challengelist[i].realm==realm:
#                    print(self.challengelist[i].due_date)
#                    print(i, self.challengelist[i].name, "\n")
                    due.append([self.challengelist[i].due_date, self.challengelist[i].name, self.challengelist[i].uniq_id])
#        for i in due:
#            print("due: ", i)
        #now sort the due list
        sorted_due=[]
        for j in due:
#            print("j", j)
            if sorted_due==[]:
                sorted_due.append(j)
            else:
                count=0
                done=0
                for k in sorted_due:
                    if done == 0:
#                        print("k", k)
#                        print("j0", j[0])
#                        print("k0", k[0])
                        if j[0]<k[0]:
                            sorted_due.insert(count, j)
                            done=1
                        count=count+1
                if done==0:
                    sorted_due.append(j)
#            print("sorted?", sorted_due)
        duedate=None
        for i in sorted_due:
            if i[0]!=duedate:
                print(i[0])
                duedate=i[0]
            print("  ", i[1], "(#", i[2], ")")

#            print("sorted_due: ", i)


    def check_duedates(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].due_date == None and self.challengelist[i].completed=="N" and self.challengelist[i].repeat=="N":
                print(self.challengelist[i].long_print())
                addit=input("Add due date? (Y/N)")
                if addit == "Y":
                    self.change_duedate(i)

    def print_todo(self, numdays, realm):
        diff=timedelta(days=numdays)
        today=datetime.datetime.combine(date.today(),datetime.time(0, 0)) 
        for step_days in range(numdays):
            day=today+timedelta(days=step_days)
            self.print_todotoday(day=day, realm=realm)


    def print_completed(self, numdays=7, realm="work"):
        today=datetime.datetime.combine(date.today(),datetime.time(0, 0)) 
        length=range(len(self.challengelist))
        daysofweek=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for step_days in range(-1*numdays, 0):
            points=0
            day=today+timedelta(days=step_days)
            dow=daysofweek[day.weekday()]
            print(dow, ", ", day)
            for i in length:
                if self.challengelist[i].date_completed==day and self.challengelist[i].realm==realm:
                    print("   ", self.challengelist[i].uniq_id, self.challengelist[i].short_print())
                    points+=float(self.challengelist[i].pt_val)
            print("total point val: ", str(points), "\n")



    def print_bosses(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].isboss=="Y" and self.challengelist[i].completed=="N":
                print("\nBOSS:", self.challengelist[i].uniq_id, self.challengelist[i].short_print())
#                print("Subchallenges:")
                for j in length:
#                    if self.challengelist[j].boss != "":
#                        print(j)
#                        print(type(self.challengelist[j].boss))
#                        print(type(i))
                    if (str(self.challengelist[j].boss) == str(self.challengelist[i].uniq_id)) and self.challengelist[j].completed=="N":
                        if self.challengelist[j].active=="N":
                            print("   (")#, end="")
                        else:
                            print("   ")#, end="")
                        print(self.challengelist[j].uniq_id, self.challengelist[j].short_print())#, end="")
                        if self.challengelist[j].active=="N":
                            print(")")
                        else:
                            print("")


    def print_challenges(self, active="Y", realm=None, subrealm=None, context=None, old=None, today=None, long_print="N"):
        length=range(len(self.challengelist))
        #set up indexes to keep track
        ind=[]
        for i in length:
            ind.append(0)
        #count keeps track of how many restrictions there are -- i.e. what "score" is for a task to be returned
        count=0

        if old!=None:
            count+=1
            today=datetime.datetime.combine(date.today(), datetime.time(0, 0))
            too_old=timedelta(days=old) #print anything that's been sitting there for more than "old" weeks
            for i in length:
                if self.challengelist[i].date_created<=today-too_old:
                    print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
                    ind[i]+=1

        if active=="Y":
            count+=1
            for i in length:
                if self.challengelist[i].active=="Y":
                    ind[i]+=1
        elif active=="N":
            count+=1
            for i in length:
                if self.challengelist[i].active=="N":
                    ind[i]+=1

        if realm!=None:
            count+=1
            for i in length:
                if self.challengelist[i].realm==realm:
                    ind[i]+=1


        if subrealm!=None:
            count+=1
            for i in length:
                if self.challengelist[i].subrealm==subrealm:
                    ind[i]+=1
                
        if context!=None:
            count+=1
            for i in length:
                if self.challengelist[i].context==context:
                    ind[i]+=1

        if today!=None:
            count+=1
            for i in length:
                if self.challengelist[i].due_date==str(datetime.datetime.combine(date.today(), datetime.time(0, 0))):
                    ind[i]+=1

        count2=0
        if long_print=="Y":
            for i in length:
                if ind[i]==count:
                   print(self.challengelist[i].uniq_id, self.challengelist[i].long_print())
                   count2+=1
        else:
            for i in length:
                if ind[i]==count:
                   print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
                   count2+=1

        print(str(count2)+" challenges")

    def print_overdue(self):
        today=datetime.datetime.combine(date.today(), datetime.time(0, 0))
        length=range(len(self.challengelist))
        first=0
        for i in length:
            if self.challengelist[i].due_date != None and self.challengelist[i].completed== "N" and self.challengelist[i].due_date<today:
                if first==0:
                    print("Overdue item(s): ")
                    first=1
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
        first=0
        for i in length:
            if self.challengelist[i].planned_date != None and self.challengelist[i].completed== "N" and self.challengelist[i].planned_date<today:
                if first==0:
                    print("Planned date passed: ")
                    first=1
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
                
    def reset_planned(self):
        today=datetime.datetime.combine(date.today(), datetime.time(0, 0))
        length=range(len(self.challengelist))
        first=0
        for i in length:
            if self.challengelist[i].planned_date != None and self.challengelist[i].completed== "N" and self.challengelist[i].planned_date<today:
                self.challengelist[i].planned_date=None
   

        
    def print_duetoday(self, day=datetime.datetime.combine(date.today(), datetime.time(0, 0))):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].due_date==day and self.challengelist[i].active=="Y":
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())

    def print_todotoday(self, day=datetime.datetime.combine(date.today(), datetime.time(0, 0)), realm="work"):
        length=range(len(self.challengelist))
        points=0
        daysofweek=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow=daysofweek[day.weekday()]
        print(dow, ", ", day)
        for i in length:
            if self.challengelist[i].planned_date==day and self.challengelist[i].active=="Y" and self.challengelist[i].realm==realm:
                print("   ", self.challengelist[i].uniq_id, self.challengelist[i].short_print())
                points+=float(self.challengelist[i].pt_val)
        print("total point val: ", str(points), "\n")

                

    def print_oldtodos(self):
        today=datetime.datetime.combine(date.today(), datetime.time(0, 0))
        too_old=timedelta(days=14) #print anything that's been sitting there for more than 2 weeks
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].active =="Y" and self.challengelist[i].date_created<=today-too_old:
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())


    def print_weeklyreview(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].active =="Y" and self.challengelist[i].subrealm=="weekly review":
#                print(i)
#                print(self.challengelist[i])
                print(self.challengelist[i].uniq_id, self.challengelist[i].short_print())
#                print(" ")

    def refresh_challenges(self):
#        today=datetime.datetime.combine(datetime.datetime.combine(date.today(), datetime.time(0, 0)), datetime.time(0, 0)) 
        today=datetime.datetime.combine(date.today(), datetime.time(0, 0))
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].active =="N" and self.challengelist[i].completed =="N":
#                print(self.challengelist[i].next_active)
               #first check if the next active date has arrived
#                print(i)
                if self.challengelist[i].next_active != None and self.challengelist[i].next_active<=today:
                    self.challengelist[i].active="Y"
                #now check if a recently completed challenge has unlocked something new
                if self.challengelist[i].unlocked_by != "" and self.challengelist[i].unlocked_by !=[]:
#                    print("in loop for item", i)
                    #TODO not unlocking challenges it should unlock
                    all_complete="Y"
#                    print("in unlocked if statement")
                    for j in self.challengelist[i].unlocked_by:
#                        print("checking unlockeds")
                        num=self.uniq2index(j)
                        if self.challengelist[num].completed=="N":
                            all_complete="N"
                    #TODO think about whether you should be able to unlock challenges that
                    #have next_active dates (i.e. this challenge is unlocked by these challenges and after this date
                    if all_complete=="Y" and (self.challengelist[i].next_active=="" or self.challengelist[i].next_active==None):
#                        print("everything is completed!")
                        self.challengelist[i].active="Y"
                        print("Congratulations, you have just unlocked challenge '"+self.challengelist[i].name+"'!")

    def save_challenges(self):
        directory=os.getcwd()
        f=open(directory+"/Life_challenge_file.txt", 'wb')
        pickle.dump(self.challengelist, f)
        f.close()
        f=open(directory+"/Life_habit_file.txt", 'wb')
        pickle.dump(self.habitlist, f)
        f.close()
        f=open(directory+'/Life_points_file.txt', 'wb')
        pickle.dump(self.record, f)
        f.close()
        f=open(directory+'/Life_preferences_file.txt', 'wb')
        pickle.dump(self.prefs, f)
        f.close()

#    def change_challenge(self, uniq_id, name=None, pt_val=None, context=None, \
#                         realm=None, subrealm=None, repeat=None)
#        index=self.uniq2index(uniq_id)
        

    def toggle_completed(self, uniq_id):

        print(uniq_id)
        print(self.challengelist[uniq_id].completed)
        if self.challengelist[uniq_id].completed=="N":
            self.complete(uniq_id)
        elif self.challengelist[uniq_id].completed=="Y":
            self.uncomplete(uniq_id)
        else:
            print("Can't change completed. Values is: ", self.challengelist[uniq_id].completed)
        print("value is now", self.challengelist[uniq_id].completed)
        value = self.challengelist[uniq_id].completed
        return value
                       
    def change_name(self, uniq_id):
        index=self.uniq2index(uniq_id)
        print("Old name was ", self.challengelist[index].name)
        new_name=input("What is the new name: ")
        self.challengelist[index].name=new_name

    def change_pt_val(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_pt_val=float(input("What is the new point val: "))
        self.challengelist[index].pt_val=new_pt_val

    def change_context(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_context=input("What is the new context: ")
        self.challengelist[index].context=new_context

    def change_realm(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_realm=input("What is the new realm: ")
        self.challengelist[index].realm=new_realm

#    def get_realm(self):
#        return self.realm!!!

    def change_subrealm(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_subrealm=input("What is the new subrealm: ")
        self.challengelist[index].subrealm=new_subrealm

    def change_repeat(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_repeat=input("What is the new repeat (Y/N:) ")
        self.challengelist[index].repeat=new_repeat

    def change_repeat_time(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_repeat_time=int(input("What is the new repeat time:  "))
        self.challengelist[index].repeat_time=new_repeat_time

    def change_repeat_reset(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_repeat_reset=int(input("What is the new repeat reset:  "))
        self.challengelist[index].repeat_reset=new_repeat_reset

    def change_isboss(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_isboss=input("Is this a boss (Y/N): ")
        self.challengelist[index].isboss=new_isboss
        
    def change_boss(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_boss=input("What boss challenge does this belong to? : ")
        self.challengelist[index].boss=new_boss

    def change_duedate(self, uniq_id):
        index=self.uniq2index(uniq_id)
        isduedate=input("Is there a due date?: Y/N ")
        if isduedate=="Y":
            new_duedate=me.get_date()
        else:
            new_duedate=None
        self.challengelist[index].due_date=new_duedate

    def change_tododate(self, uniq_id, day=0):
        index=self.uniq2index(uniq_id)
        if day == 0:
            new_tododate=me.get_date()
        else:
            new_tododate=day
        self.challengelist[index].planned_date=new_tododate

    def change_comments(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_comments=input("comments: ")
        self.challengelist[index].comments=new_comments

    def change_active(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_active=input("Active (Y/N:) ")
        self.challengelist[index].active=new_active

    def change_activedate(self, uniq_id):
        index=self.uniq2index(uniq_id)
        new_active=me.get_date()
        self.challengelist[index].next_active=new_active

    def change_unlockedby(self, uniq_id):
        index=self.uniq2index(uniq_id)
        AR=input("add (A) or remove (R)? ")
        if AR == "A":
            value=input("what other challenges are required to unlock this challenge? (one at a time, 'Q' to quit):")
            while value !="Q" and value!="":
                self.challengelist[index].unlocked_by.append(int(value))
                self.challengelist[index].active="N"
                value=input("what other challenges are required to unlock this challenge? (one at a time, 'Q' to quit):")

        if AR == "R":
            remove=input("remove all (the only choice at this point)?")
            if remove == "Y":
                self.challengelist[index].unlocked_by=[]
            else:
                print("That's cool.")


    def add_challenges(self):
        next="Y"
        while next == "Y":
            self.add_challenge()
            next=input("Add another? (Y/N)")

    def check_bosses(self):
        length=range(len(self.challengelist))
        for i in length:
            if self.challengelist[i].isboss=="N" and self.challengelist[i].repeat=="N" and self.challengelist[i].completed=="N":
                print("\n", self.challengelist[i].uniq_id, self.challengelist[i].short_print())
                isboss=input("Do you want to make this challenge a boss? (Y/N)?")
                if isboss == "Y":
                    self.challengelist[i].isboss="Y"
            #make bosses locked until all their children are completed
            if self.challengelist[i].isboss=="Y":
                for j in length:
                    if (self.challengelist[j].boss == str(self.challengelist[i].uniq_id)) and self.challengelist[j].completed=="N":
                        self.challengelist[i].unlocked_by.append(j)
                        self.challengelist[i].active="N"
                        #if boss is due by certain date, all children are also due by that date
                        self.challengelist[j].due_date=self.challengelist[i].due_date
            #if something is not listed as a boss, but someone else calls it a boss, make it a boss
            #TODO -- something isn't working right with next loop -- not picking out some non-bosses that are called bosses
            if self.challengelist[i].boss !="":
                thisisaboss=self.challengelist[i].boss
                if type(thisisaboss)==int and self.challengelist[thisisaboss].isboss=="N":
                    print(thisisaboss, self.challengelist[thisisaboss].name, " is called a boss by ", i, self.challengelist[i].name)
                    makeboss=input("Make it a boss? Y/N ")
                    if makeboss=="Y":
                        self.challengelist[thisisaboss].isboss="Y"
            #TODO -- need to also check that bosses are planned to be completed later than minions

    def occasional_challenge_sets(self, file_name=None, NLE="L"):
#        print("testing issues")
#        file_name=input("What is a the file name? ")
#        NLE=input("Are you creating a new file (N), loading a file (L) or editing a file (E)?")
        #load the file
        directory=os.getcwd()
        if NLE=="L" or NLE == "E":
            while file_name==None:
                file_name=input("What is the file name?")
            f=open(directory+"/"+file_name, mode='rb')
            challenge_set=pickle.load(f)
            f.close()
        if NLE=="E":
            length=range(len(challenge_set))
            for i in length:
                print(i, challenge_set[i].name, challenge_set[i].pt_val, challenge_set[i].due_date)
            doedit=input("Edit one of these challenges?(Y/N)")
            while doedit=="Y":
                num=int(input("Which challenge? "))
                val=input("Name (N), points (P), due time (D)? ")
                if val=="N":
                    new_name=input("What's the new name? ")
                    challenge_set[num].name=new_name
                if val=="P":
                    new_pts=input("What is the new point value? ")
                    challenge_set[num].pt_val=float(new_pts)
                if val=="D":
                    new_duedate=input("What is the new duetime (vs target date)? ")
                    challenge_set[num].due_date=new_duedate
                doedit=input("Edit another challenge? (Y/N)")
        if NLE=="N":
            challenge_set=[]
            realm=input("realm (work): ")
            if realm == "":
                realm="work"
            subrealm=input('subrealm (none): ')
            if subrealm == "":
                subrealm="none"
            print("First task entered will be the boss challenge")
            more="Y"
            first=1
        if NLE=="E":
            first=0
            realm=challenge_set[0].realm
            subrealm=challenge_set[0].subrealm
            more=input("Add another task (Y/N)?")
            
        if NLE == "N" or NLE=="E":
            first_index=0
            while more=="Y":                    
                name=input('Name: ')
                pt_val=input('Point value (default 1): ')
                if pt_val == "":
                    pt_val=1
                pt_val=float(pt_val)
                notes=input('Notes? ')
                context=input('context (none): ')
                if context == "":
                    context=None
                repeat=input('repeat (Y/N): ')
                if repeat == "Y":
                    repeat_time=input("repeat time (days, default=1): ")
                    if repeat_time== "":
                        repeat_time=1
                    repeat_time=int(repeat_time)
                    repeat_reset=int(input("repeat reset(0=repeats from last appeared, 1=repeats from last completed): "))
                    while repeat_reset=="":
                        repeat_reset=int(input("repeat reset(0=repeats from last appeared, 1=repeats from last completed): "))
                else:
                    repeat_time=None
                    repeat_reset=None
                if first==1:
                    isboss="Y"
                else:
                    isboss="N"
                if first==0:
                    boss=None
                else:
                    boss=0


                date_created=None
                date_last_comp=None
                unlocked_by=[]
                value=input("what other challenges are required to unlock this challenge? (one at a time, 'Q' to quit, default none): ")
                while value !="Q" and value!="":
                    unlocked_by.append(int(value))
                    value=input("what other challenges are required to unlock this challenge? (one at a time, 'Q' to quit):")
        
                due_date=int(input("What is the due date compared to the target date? "))
                next_active=int(input("What is the active date compared to the target date? "))

                planned_date=None
                completed="N"
                date_completed=None
                active="N"
                comments=None

                challenge_set.append(task(name, notes, context, pt_val, realm.lower(), subrealm.lower(), repeat, repeat_time, \
                                  repeat_reset, isboss, boss, date_created, date_last_comp, \
                                  due_date, completed, date_completed, active, next_active, \
                                  comments, unlocked_by, planned_date, len(me.challengelist)))
                print(challenge_set[0].name)

                first=1

                more=input("Add another task (Y/N)? ")
        saveit=input("Save this challenge set (Y/N)? ")
        if saveit=="Y":
            f=open(directory+file_name, 'wb')
            pickle.dump(challenge_set, f)
            f.close()
            
        activate=input("Activate challenge (Y/N)? ")
        if activate=="Y":
            name_here=input("Name of this instance of the challenge")
            challenge_set[0].name=name_here
            print("Input target date.")
            target_date=me.get_date()
            length=range(len(challenge_set))
            first=0
            first_index=0
            for i in length:
                date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)) 
                date_diff=timedelta(challenge_set[i].due_date) 
                due_date=target_date+date_diff
                active_diff=timedelta(challenge_set[i].next_active) 
                next_active=target_date+active_diff
                if challenge_set[i].unlocked_by==[] and next_active<=datetime.datetime.combine(date.today(), datetime.time(0, 0)) :
                    active="Y"
                else:
                    active="N"
                if first==0:
                    boss=None
                else:
                    boss=first_index
                index=self.add_challenge(name=challenge_set[i].name, notes=challenge_set[i].notes, \
                                   context=challenge_set[i].context,\
                                   pt_val=challenge_set[i].pt_val,\
                                   realm=challenge_set[i].realm,\
                                   subrealm=challenge_set[i].subrealm,\
                                   repeat=challenge_set[i].repeat,\
                                   repeat_time=challenge_set[i].repeat_time,\
                                   repeat_reset=challenge_set[i].repeat_reset, \
                                   isboss=challenge_set[i].isboss,\
                                   boss=boss,\
                                   date_created=date_created,\
                                   date_last_comp=challenge_set[i].date_last_comp,\
                                   due_date=due_date,\
                                   completed=challenge_set[i].completed,
                                   date_completed=challenge_set[i].date_completed,\
                                   active=active, \
                                   next_active=next_active,\
                                   comments=challenge_set[i].comments,\
                                   unlocked_by=[],\
                                   planned_date=challenge_set[i].planned_date)
                if challenge_set[i].unlocked_by !=0 and first==1: #boss challenge can't have unlocked by
                    self.challengelist[index].unlocked_by=challenge_set[i].unlocked_by+first_index
                    
                if first == 0:
                    first_index=len(self.challengelist)-1
                    first=1
                                                          
    def add_subchallenge(self, uniq_id):
        num=self.uniq2index(uniq_id)
        
        length=range(len(self.challengelist))
        bosschal=[]
        for i in length:
            if self.challengelist[i].uniq_id == num:
                bosschal.append(i)
        if len(bosschal) >1:
            print("more than one challenge match that number")
            return
        if len(bosschal)==0:
            print("no challenge found")
            return
        bosschal=int(bosschal[0])
        
        self.add_challenge(realm=self.challengelist[bosschal].realm,\
                      subrealm=self.challengelist[bosschal].subrealm, \
                      isboss='N', boss=bosschal, unlocked_by=[])


        chal_num=len(self.challengelist)

        #since this is a subchallenge, the main challenge should be unlocked by this subchallenge
        self.challengelist[bosschal].unlocked_by.append(self.challengelist[chal_num-1].uniq_id)
        self.challengelist[bosschal].isboss='Y'

        self.save_challenges()

    def add_habit(self, name=None, pt_val=None, notes=None, context=None, realm="None",\
                      subrealm="None", repeat="Y", repeat_time=1, repeat_reset=None,\
                      isboss=None, boss=None, unlocked_by=None, date_last_comp=[],\
                      next_active=None, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)), due_date="", active="Y", planned_date="", completed='N'):

        #keep track of uniq_ids so I can later make the app work using keys instead of just mouse ("click C for complete then the task number", Click A for add then the habit number")
    
        print("adding a habit")
        comments=[]
        chal_num=len(self.habitlist)
        #uniq_id is just one more than previous challenge
        if chal_num > 0:
            uniq_id=self.habitlist[chal_num-1].uniq_id+1
        elif chal_num==0:
            uniq_id=0
        else:
            print("this list has a negative length")


        self.habitlist.append(task(name=name, notes=notes, context=context, \
                                       pt_val=pt_val, realm=realm.lower(), \
                                       subrealm=subrealm.lower(), repeat=repeat, \
                                       repeat_time=repeat_time, \
                                       repeat_reset=repeat_reset, isboss=isboss,\
                                       boss=boss, date_created=date_created, \
                                       date_last_comp=date_last_comp, \
                                       due_date=due_date, completed=completed, \
                                       date_completed="", active=active, \
                                       next_active=next_active, \
                                       comments=comments, unlocked_by=unlocked_by, \
                                       planned_date=planned_date, uniq_id=uniq_id))
        self.save_challenges()


    def add_challenge_basic(self, name=None, pt_val=None, notes=None, context=None, realm="None",\
                      subrealm="None", repeat=None, repeat_time=None, repeat_reset=None,\
                      isboss=None, boss=None, unlocked_by=None, date_last_comp=[],\
                      next_active=None, date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)), due_date="", active="Y", planned_date="", completed='N'):
        comments=[]
        chal_num=len(self.challengelist)
        #uniq_id is just one more than previous challenge
        if chal_num > 0:
            uniq_id=self.challengelist[chal_num-1].uniq_id+1
        elif chal_num==0:
            uniq_id=0
        else:
            print("this list has a negative length")
#        date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0))
        date_completed=""
#        print("adding challenge")
#        print("name: ", name)
#        print("realm: ", realm)
#        print("pts: ", pt_val)
#        print("uniqid", uniq_id)
        self.challengelist.append(task(name=name, notes=notes, context=context, \
                                       pt_val=pt_val, realm=realm.lower(), \
                                       subrealm=subrealm.lower(), repeat=repeat, \
                                       repeat_time=repeat_time, \
                                       repeat_reset=repeat_reset, isboss=isboss,\
                                       boss=boss, date_created=date_created, \
                                       date_last_comp=date_last_comp, \
                                       due_date=due_date, completed=completed, \
                                       date_completed=date_completed, active=active, \
                                       next_active=next_active, \
                                       comments=comments, unlocked_by=unlocked_by, \
                                       planned_date=planned_date, uniq_id=uniq_id))
        self.save_challenges()
        print("This will be challenge #", uniq_id)
        if uniq_id==1000:
            print("CONGRATULATIONS!!  You've won a badge for adding 1000 challenges!")
            #todo make a way to keep track of badges
        return uniq_id
    
        
    def add_challenge(self, name=None, pt_val=None, notes=None, context=None, realm=None,\
                      subrealm=None, repeat=None, repeat_time=None, repeat_reset=None,\
                      isboss=None, boss=None, unlocked_by=None, date_last_comp=[],\
                      next_active=None, due_date="", active="Y", planned_date="", completed='N'):
##        if name == None:
##            name=input('Name: ')
##        if pt_val == None:
##            pt_val=input('Point value (default 1): ')
##            if pt_val == "":
##                pt_val=1
##            pt_val=float(pt_val)
##        if notes == None:
##            notes=input('Notes? ')
##        if context == None:
##            context=input('context (none): ')
##            if context == "":
##                context="none"
##        if realm == None:
##            realm=input('realm (work): ')
##            if realm == "":
##                realm="work"
##            if realm not in self.prefs.realm_names:
##                print("This realm is not in realm names -- option to add realms not yet available ")
##                print(self.prefs.realm_names)
##                #todo add ability to change/add/remove realms
##                realm=input("realm? ")
##        if subrealm == None:
##            subrealm=input('subrealm (none): ')
##            if subrealm == "":
##                subrealm="none"
##        while repeat !='N' and repeat !='Y':
##            repeat=input('repeat (Y/N): ')
##        if repeat == "Y":
##            if repeat_time==None:
##                repeat_time=input("repeat time (days, default=1): ")
##                if repeat_time== "":
##                    repeat_time=1
##                repeat_time=int(repeat_time)
##            if repeat_reset==None:
##                repeat_reset=int(input("repeat reset(0=repeats from last appeared, 1=repeats from last completed): "))
##                while repeat_reset=="":
##                    repeat_reset=int(input("repeat reset(0=repeats from last appeared, 1=repeats from last completed): "))
##        else:
##            repeat_time=None
##            repeat_reset=None
##
##        if isboss == None:
##            isboss=input("is this a boss challenge (Y/N): ")
##            while isboss=="":
##                isboss=input("is this a boss challenge (Y/N): ")
##        if boss == None:
##            boss=input("what boss challenge does this belong to (none): ")
##
        date_created=datetime.datetime.combine(date.today(), datetime.time(0, 0)) 
##        if unlocked_by==None:
##            unlocked_by=[]
##            value=input("what other challenges are required to unlock this challenge? (one at a time, 'Q' to quit, default none): ")
##            while value !="Q" and value!="":
##                unlocked_by.append(int(value))
##                value=input("what other challenges are required to unlock this challenge? (one at a time, 'Q' to quit):")
##        if due_date=="":        
##            isduedate=input("Is there a due date?: Y/N ")
##            if isduedate=="Y":
##                due_date=me.get_date()
##            else:
##                due_date=None
##        if planned_date=="":
##            isplanneddate=input("Add date to work on this?(Y/N) ")
##            if isplanneddate=="Y":
##                planned_date=me.get_date()
##            else:
##                planned_date=None
##        if completed == "Y":
##            date_completed=[datetime.datetime.combine(date.today(), datetime.time(0, 0))]
        date_completed=""
##        if unlocked_by!=[]: 
##            active="N"
        comments=[]
        chal_num=len(self.challengelist)
        #uniq_id is just one more than previous challenge
        uniq_id=self.challengelist[chal_num-1].uniq_id+1
        self.challengelist.append(task(name=name, notes=notes, context=context, \
                                       pt_val=pt_val, realm=realm.lower(), \
                                       subrealm=subrealm.lower(), repeat=repeat, \
                                       repeat_time=repeat_time, \
                                       repeat_reset=repeat_reset, isboss=isboss,\
                                       boss=boss, date_created=date_created, \
                                       date_last_comp=date_last_comp, \
                                       due_date=due_date, completed=completed, \
                                       date_completed=date_completed, active=active, \
                                       next_active=next_active, \
                                       comments=comments, unlocked_by=unlocked_by, \
                                       planned_date=planned_date, uniq_id=uniq_id))
        me.save_challenges()
        print("This will be challenge #", uniq_id)
        if uniq_id==1000:
            print("CONGRATULATIONS!!  You've won a badge for adding 1000 challenges!")
            #todo make a way to keep track of badges
        return uniq_id


    def get_date(self):
        isValid=False
        while not isValid:
            userIn = input("Type Date m/d/yy: ")
            try: # strptime throws an exception if the input doesn't match the pattern
                thedate = datetime.datetime.strptime(userIn, "%m/%d/%y")
                isValid=True
            except ValueError:
                print("Try again! m/d/yy\n")
        return thedate


class task(object):
    def __init__(self, name=None, notes=None, context=None, pt_val=None, realm=None, subrealm=None, repeat=None, \
                 repeat_time=None, repeat_reset=None, isboss=None, boss=None, date_created=None, \
                 date_last_comp=None, due_date=None, completed="N", date_completed=None, active=None, \
                 next_active=None, comments=None, unlocked_by=None, planned_date=None, uniq_id=None):
        self.name=name
        self.notes=notes
        self.pt_val=pt_val
        self.context=context
        self.realm=realm
        self.subrealm=subrealm
        self.repeat=repeat
        self.repeat_time=repeat_time #1=1 day, need more sophisticated for monthly, etc at some point.
        self.repeat_reset=repeat_reset 
        self.isboss=isboss
        self.boss=boss
        self.date_created=date_created
        self.date_last_comp=date_last_comp
        self.due_date=due_date
        self.completed=completed
        self.date_completed=date_completed
        self.active=active
        self.next_active=next_active
        self.comments=comments
        self.unlocked_by=unlocked_by
        self.planned_date=planned_date
        self.uniq_id=uniq_id

    def short_print(self):
        return "(%s) %s" % (self.pt_val, self.name)

    def long_print(self):
        return "Name: %s\nnotes: %s\nlocation: %s\npoint value: %s\nrealm: %s\nsubrealm:%s\nrepeat:%s\n\
repeat_time:%s\nrepeat_reset:%s\nisboss:%s\nboss:%s\ndate_created:%s\ndate_last_comp:%s\ndue_date:%s\n\
completed:%s\nactive: %s\nnext_active: %s\nrequires:%s\nuniq_id:%s\ncomments:%s\n" % (self.name, self.notes, self.context, self.pt_val, self.realm, \
                                                                self.subrealm, self.repeat, self.repeat_time, \
                                                                self.repeat_reset, self.isboss, self.boss, \
                                                                self.date_created, self.date_last_comp, \
                                                                self.due_date, self.completed, self.active, \
                                                                self.next_active, self.unlocked_by, self.uniq_id, self.comments)

    def __str__(self):
        
        return "Name: %s     point value: %s  realm: %s   subrealm: %s   \
isboss:%s     boss: %s   due_date: %s" % (self.name, self.pt_val, self.realm, \
                                                                self.subrealm,   \
                                                                self.isboss, self.boss, \
                                                                self.due_date)



"""    def long_print(self):
        return "Name: %s\nlocation: %s\n point value: %s\n realm: %s\n subrealm:%s\n repeat:%s\n \
repeat_time:%s\n repeat_reset:%s\n isboss:%s\n boss:%s\n date_created:%s\n date_last_comp:%s\n due_date:%s\n \
d:%s\n active: %s\n next_active: %s\n comments:%s\n" % (self.name, self.context, self.pt_val, self.realm, \
                                                                self.subrealm, self.repeat, self.repeat_time, \
                                                                self.repeat_reset, self.isboss, self.boss, \
                                                                self.date_created, self.date_last_comp, \
                                                                self.due_date, self.completed, self.active, \
                                                                self.next_active, self.comments)"""
class points(object):
    def __init__(self, date, realm_pts):
        today=datetime.datetime.combine(date.today(), datetime.time(0, 0)) 
        yesterday=timedelta(days=-1)+datetime.datetime.combine(date.today(), datetime.time(0, 0))
#        print("yesterday", yesterday)
#        print("next item", datetime.datetime.combine(date.today(), datetime.time(0, 0)),datetime.time(0, 0))
#        self.date=[yesterday, today]
        self.date=[yesterday, datetime.datetime.combine(date.today(), datetime.time(0, 0))]

#  the next line is the original but gave an error
#        self.date=[yesterday, datetime(datetime.datetime.combine(date.today(), datetime.time(0, 0)),datetime.time(0, 0)) ]
#        self.pts=[0, pts]
        self.realm_pts=[[0, 0, 0, 0], realm_pts]


class prefs(object):
    def __init__(self, num_realms, num_subrealms, realm_names, ideal_pts):
         self.num_realms=num_realms
         self.num_subrealms=num_subrealms
         self.realm_names=realm_names
         self.ideal_pts=ideal_pts
# the test data ...
me=avatar()
#me.add_challenge_basic(name="read in helio data in python", context="computer", pt_val=5, realm="Work", subrealm="Helio", \
#repeat="N", repeat_time=0, repeat_reset=0, isboss="N", boss="NR", date_created=date.today())
##root=tk.Tk()
##root.title("question time")
##
##Yesno_question_window(root, "What's up?")
##
##root.wait_window(Yesno_question_window.top)
##
##print("Answer is!: ", Yesno_question_window.answer)

#TODO: this should be configurable -- changeable -- should be able to just change it as needed, but should save in prefs

view_header=['Task #', 'name', 'realm', 'context', 'points', 'due date']
habit_header=['Habit #', 'name', 'realm', 'context', 'points']


def about_box():
    print("This gui works to keep track of your todo list")

def change_column_views():
    print("coming soon")
    
def view_subset():
    ###TODO creates popup menu that allows you to select one more more subsets/contexts
    print("coming soon")

def view_plan():
     print("coming soon")   

def view_tasks():
     print("coming soon") 

def view_points():
     print("coming soon") 
      
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Todolist manager")
    menubar=tk.Menu(root)
    filemenu=tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="About", command=about_box)
    filemenu.add_command(label="Quit", command=root.destroy)
    menubar.add_cascade(label="File", menu=filemenu)

    viewmenu=tk.Menu(menubar, tearoff=0)
    viewmenu.add_command(label="view subset", command=view_subset)
    viewmenu.add_command(label="plan next week", command=view_plan)
    viewmenu.add_command(label="task view", command=view_tasks)
    viewmenu.add_command(label="points view", command=view_points)
    viewmenu.add_command(label="change column view", command=change_column_views)
    menubar.add_cascade(label="View", menu=viewmenu)

#    menubar.add_command(label="About", command=about_box)
#    menubar.add_command(label="View", command=change_view)
#    menubar.add_command(label="Quit", command=root.destroy)
    root.config(menu=menubar)
    listbox = MultiColumnListbox(root)
    tk.mainloop()

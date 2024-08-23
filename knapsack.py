######################################
#                                    #
#     Knapsack - Password Manager    #
#       created by Kevin Hansen      #
#        GNU Public Licence v.3      #
#                                    #
######################################
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter.messagebox import showinfo
import sqlite3
import os
import sys
import random
import time
from bs4 import BeautifulSoup as bs
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    
dbfile = application_path.replace("\\", "/") + "/passwords.db"
con = sqlite3.connect(dbfile)
cur = con.cursor()
try:
    # create the table 'password' if it does not exist
    cur.execute("CREATE TABLE password(pw, username, site)")
except:
    pass
    
def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
        
def writeTable(pwd, unamer, siter):
    line = "INSERT INTO password VALUES('" + pwd.replace("&amp;", "&") + "', '" + unamer + "', '" + siter + "')"
    cur.execute(line)
    con.commit()
    
def readTable(self):
    try:
        self.password.clear()
        self.username.clear()
        self.sitename.clear()
    except:
        pass
    line = "SELECT pw, username, site FROM password"
  
    for row in cur.execute(line):
        self.password.append(row[0])
        self.username.append(row[1])
        self.sitename.append(row[2])
        
def tableBackup(self):
    try:
        self.password.clear()
        self.username.clear()
        self.sitename.clear()
    except:
        pass
    
    line = "SELECT pw, username, site FROM password"
  
    for row in cur.execute(line):
        self.password.append(row[0])
        self.username.append(row[1])
        self.sitename.append(row[2])
    
        
def deleteRow(self, pw, site):
    line = "DELETE FROM password WHERE pw='" + pw + "' AND site='" + site + "'"
    cur.execute(line)
    con.commit()
    time.sleep(1)
    readTable(self)
    self.show_pws()

class Passwords(tk.Tk):
    sizes = []
    choices = []
    password = []
    username = []
    sitename = []
    
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    
    def update_pws(self, i):
        line = "UPDATE password SET pw='" + self.entr.get() + "' WHERE username='" + self.username[i] + "' AND site='" + self.sitename[i] + "'"
        cur.execute(line)
        con.commit()
        self.pwlabs[i]['text'] = self.entr.get()
    
    def about(self):
        def closeme():
            mroot.destroy()
            
        mroot = tk.Frame(self, bg="black")#, width=self.winfo_width()-10)
        mroot.place(relx = 0.5, rely = 0.5, anchor = "center")
        
        titlelab = tk.Label(mroot, text="Knapsack - Password Manager", font="Times 15", bg="black", fg="white", width=self.winfo_width()-10)
        titlelab.pack(side="top", padx = 10, pady = (10, 0), fill="x")
        
        verslab = tk.Label(mroot, text="Version 1.0\n\nWritten by Kevin Hansen", font="Times 13", bg="black", fg="white", width=self.winfo_width()-10)
        verslab.pack(side="top", padx=10, pady=0, fill="x")
        
        datelab = tk.Label(mroot, text="Updated: 8/22/2024", font="Times 10", bg="black", fg="white", width=self.winfo_width()-10)
        datelab.pack(side="top", padx=10, pady=0, fill="x")
        
        info = "Knapsack password manager was designed to create, store, and organize unique and random passwords. Dislike coming up with strong passwords? The generate button makes it easy for you. Never lose or forget your passwords again.Convenient one click copy feature on passwords and usernames. Need to change a password, simply click on generate to create a new password then click the update button in line with the corresponding password."
        
        infolab = tk.Label(mroot, text=info, font="Times 12", bg="black", fg="white", wraplength=self.winfo_width()-10)
        infolab.pack(side="top", padx=10, pady=10, fill="x")
        
        gnu = """GNU Public Licence\n\nThis program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or at your option any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program. If not, see \nhttps://www.gnu.org/licenses"""
        gnulab = tk.Label(mroot, text=gnu, font="Times 12", wraplength=self.winfo_width()-10)
        gnulab.pack(side="top", fill="x")
        
        cbut = tk.Button(mroot, text=" Close ", bg="white", font="Times 14", command=closeme)
        cbut.pack(side="top", pady=10)
        
        
    def export_to_file(self):
        #xmlfile1 = self.application_path.replace("\\", "/") + "/backup.xml"
        p = asksaveasfile(title = "Save your backup", initialfile = "backup.xml", initialdir = self.application_path, defaultextension = ".xml") 
        tableBackup(self)
        if p:
            p.write("<backup>\n")
            i = 0
            while i < len(self.password):
                p.write("    <info>\n")
                p.write("        <password>" + self.password[i].replace("&", "&amp;") + "</password>\n")
                p.write("        <username>" + self.username[i] + "</username>\n")
                p.write("        <sitename>" + self.sitename[i] + "</sitename>\n")
                p.write("    </info>\n")
                i += 1
            p.write("</backup>")
            p.close()
        
            
    def import_from_file(self):
        # Delete current table data before importing new data
        li = "DELETE FROM password"
        cur.execute(li)
        con.commit()
        
        # open a file dialog to open the backup xml file
        xmlfile = askopenfilename(title = "Open your backup", initialdir = self.application_path, defaultextension = ".xml") 
        
        # open and read the xml file with beautifulsoup
        with open(xmlfile, "r") as file:
            content = file.readlines()
            content = "".join(content)
            soup = bs(content, features="xml")
        x = soup.findAll("password")
        y = soup.findAll("username")
        z = soup.findAll("sitename")
        
        # populate the table with new data from the file
        i = 0
        while i < len(x):
            writeTable(x[i].text, y[i].text, z[i].text)
            i += 1
        
    def focOut(self, col, lab):
        # return the label text to a normal color/state
        lab['background'] = col
        lab.config(state='normal')
        
    def frameFocus(self, fr):
        # send focus away from highlighted text to trigger focOut
        fr.focus_set()
        
    def show_pws(self):
        # method for sizing the scroll area of the canvas      
        def onFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        windowColor = "#3d4450"
        centerColor = "#949194"
        
        try:
            # clear all child widgets from frame so new password info can fill it
            clearFrame(self.results_frame)
        except:
            pass
        
        # store canvas and frame sizes in an array on first run 
        # so it can be called from outside the class and retain 
        # accurate integers
        if len(self.sizes) == 0:
            self.update()
            x = self.winfo_height()
            y = self.winfo_width()
            ww = x - self.topFrame.winfo_height()
            self.sizes.append(x)
            self.sizes.append(y)
            self.sizes.append(ww)
        else:
            x = self.sizes[0]
            y = self.sizes[1]
            ww = self.sizes[2]
        
        canvas=tk.Canvas(self.results_frame, background = centerColor, width=y, height=ww)
        frame=tk.Frame(canvas, width=y, background="black")
        self.update_buts = []
        self.pwlabs = []
        i = 0
        while i < len(self.password):
            if i % 2 == 0:
                mycolor = centerColor
            else:
                mycolor = windowColor

            # frame changes color on every other row
            newframe = tk.Frame(frame, background=mycolor, width=y)
            newframe.bind('<Button-1>', lambda e, nf=newframe: self.frameFocus(nf))
            newframe.pack(side="top", fill="x")
            
            # password label
            pwlab = tk.Label(newframe, text=self.password[i], bg=mycolor, width=15, fg="white", font="Times 16")
            pwlab.bind('<Button-1>', lambda e, lab=pwlab: self.focusText(lab))
            pwlab.bind('<FocusOut>', lambda e, col=mycolor, lab=pwlab: self.focOut(col, lab))
            pwlab.pack(side="left", padx=10, pady=10, fill="x")
            self.pwlabs.append(pwlab)
            
            # username label
            uslab = tk.Label(newframe, text=self.username[i], bg=mycolor, width=15, fg="white", font="Times 16")
            uslab.bind('<Button-1>', lambda e, lab=uslab: self.focusText(lab))
            uslab.bind('<FocusOut>', lambda e, col=mycolor, lab=uslab: self.focOut(col, lab))
            uslab.pack(side="left", padx=10, pady=10, fill="x")
            
            # sitename label
            stelab = tk.Label(newframe, text=self.sitename[i], bg=mycolor, width=15, fg="white", font="Times 16")
            stelab.bind('<Button-1>', lambda e, nf=stelab: self.frameFocus(nf))
            stelab.pack(side="left", padx=10, pady=10, fill="x")
            
            # delete button used to remove unwanted password entries
            del_but = tk.Button(newframe, text="Delete", bg="black", fg="white", command=lambda pwds=self.password[i], ste=self.sitename[i], self=self: deleteRow(self, pwds, ste))
            del_but.pack(side="right", padx=(5, 35), pady=10)
            
            self.update_but = tk.Button(newframe, text="Update", bg="black", fg="white", command=lambda i=i: self.update_pws(i))
            self.update_but.pack(side="right", padx=5, pady=10)
            self.update_but['state'] = "disable"
            self.update_buts.append(self.update_but)
            i += 1
        
        myscrollbar=ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        canvas.pack(side="left", fill="both", expand=1)
        canvas.create_window((0,0), window=frame, anchor="nw", width=y)
        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        self.results_frame.update()
        
    def retrieve(self):
        readTable(self)
        self.show_pws()
        
    def randomize(self, lst):
        temp = []
        i = 0
        while i < 3:
            ran = random.randint(0, len(lst) - 1)
            if lst[ran] not in temp:
                temp.append(lst[ran])
                i = i + 1
            else:
                pass
        return temp
        
    # method to generate randomized passwords
    def generate(self):
        # turn the password font color from gray to black to show it is now usable
        self.pw_entry['foreground'] = "black"
        
        # Make the "update" buttons usable
        try:
            for s in self.update_buts:
                s['state'] = "normal"
        except:
            pass
            
        # instantiate the lists that will be used to form the random password
        sym = []
        num = []
        ba = []
        sa = []
        pw = []
        
        # instantiate the string variable that will form the password
        password = ""
        
        # Lists that hold all of the characters that will be used to form the password
        symbols = ["!", "@", "#", "$", "%", "&", "*", "?"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        bigAlph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        smallAl = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        
        # Grab 3 random characters from each of the lists
        sym = self.randomize(symbols)
        num = self.randomize(numbers)
        ba = self.randomize(bigAlph)
        sa = self.randomize(smallAl)
        
        # combine all randimized sublists into one password list
        pw = sym + num + ba + sa
        
        # Randomize the password list
        pw = sorted(pw, key=lambda x: random.random())
        
        # Build a string from the password list
        for p in pw:
            password = password + p
            
        # store the new password in the StringVar self.entr
        self.entr.set(password)
        
    # method used to clear and reset all user input fields
    def clear(self):
        # turn "password" in password entry gray
        self.pw_entry['foreground'] = "gray"
        
        # disable all of the "update" buttons
        try:
            for s in self.update_buts:
                s['state'] = "disable"
        except:
            pass
            
        # restore the StringVars to their original states
        self.entr.set("password")        
        self.user.set("")        
        self.site.set("")
       
    # method to write all user input into database       
    def save(self):
        x = self.entr.get()
        y = self.user.get()
        z = self.site.get()
        
        # if any of the fields are empty display a pop up warning
        if x == "password" or len(y) == 0 or len(z) == 0:
            if y == "" and z == "" and x != "password":
                msg = "User name and site name fields are empty"
            elif y == "" and z == "" and x == "password":
                msg = "Several fields are empty"
            elif x == "password" and y == "":
                msg = "Password and site name fields are empty"
            elif x == "password" and z == "":
                msg = "Several fields are empty"
            elif x == "password" or len(x) == 0 or x == "":
                msg = "Password field cannot be 'password' or empty"
            elif len(y) == 0:
                msg = "Site name cannot be empty"
            elif len(z) == 0:
                msg = "User name cannont be empty"
            
            # show the message
            showinfo("Attention", msg)
        else:
            # if all fields are filled in then write them to database and display the 
            # new results
            writeTable(x, y, z)
            readTable(self)
            self.show_pws()
            
    # method to copy the highlighted password or username to clipboard
    def copy(self, passw):
        self.clipboard_clear()
        self.clipboard_append(passw)
    
    # method to focus on text that will then be copied to clipboard
    def focusText(self, lab):        
        lab['background'] = 'dark gray'
        lab.focus_set()
        lab.config(state='disabled')
        self.copy(lab['text'])

    def __init__(self):
        tk.Tk.__init__(self)
        
        # Color Variables
        windowColor = "#3d4450"
        centerColor = "#949194"
        
        # Main Window
        self.title("Knapsack - Password Manager")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        ww = (screen_width/2) + 120
        hh = (screen_height/2) + 240
        xx = int(ww/2) - 120
        yy = int(hh/2) - 270
        self.geometry('%dx%d+%d+%d' % (ww, hh, xx, yy))
        self.configure(bg=windowColor)
        
        # Menu bar
        menubar = Menu(self)
        self.configure(menu=menubar)

        # create a menu
        file_menu = Menu(menubar, tearoff=False)

        # add menu items to the file_menu
        file_menu.add_command(label='Export to file', command=self.export_to_file)
        file_menu.add_command(label='Import from file', command=self.import_from_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.destroy)
        
        # add the File menu to the menubar
        menubar.add_cascade(label="File", menu=file_menu)
        
        # create Help and About for the menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='About', command=self.about)
        menubar.add_cascade(label="Help", menu=help_menu)
        

        # String variables to hold user input from entry fields
        self.entr = tk.StringVar()
        self.entr.set("password")
        
        self.user = tk.StringVar()
        self.user.set("")
        
        self.site = tk.StringVar()
        self.site.set("")
        
        # frames for storing widgets 
        self.topFrame = tk.Frame(self, bg=windowColor, width=ww, height=10)
        self.topFrame.pack(side="top", fill='x', anchor='n', pady=5, padx=5)
        
        pw_frame = tk.Frame(self.topFrame, bg=windowColor)
        pw_frame.pack(side="top", anchor="nw")
        
        seperate_frame = tk.Frame(self.topFrame, bg=windowColor)
        seperate_frame.pack(side="top", anchor='nw', fill="x")
        
        user_site = tk.Frame(self.topFrame, bg=windowColor)
        user_site.pack(side="top", anchor="nw", pady=(20, 10))
        
        bottom_us = tk.Frame(self.topFrame, bg=windowColor)
        bottom_us.pack(side="top", anchor="nw", pady=5, fill="x")
        
        self.results_frame = tk.Frame(self.topFrame, bg=windowColor, width=ww)
        self.results_frame.pack(side="top", anchor="nw", fill="x")
        
        # label displaying the text 'password:'
        pw_label = tk.Label(pw_frame, text="Password:  ", bg=windowColor, fg="white", font="Times 12")
        pw_label.pack(side="left", pady=(0, 10))
        
        # entry to display the randomized password
        self.pw_entry = tk.Entry(pw_frame, textvariable=self.entr, width=20, fg="gray", font="Times 12")
        self.pw_entry.pack(side="left", padx=5, pady=5)
        
        # button to generate randomized password 
        pw_button = tk.Button(pw_frame, text="  Generate  ", bg="#181818", fg="white", font="Times 12", command=self.generate)
        pw_button.pack(side="left", padx=5, pady=5)
        
        # vertical seperator
        ttk.Separator(pw_frame, orient='vertical').pack(side='left', fill='y')
        
        # button to clear all of the fields
        clear_button = tk.Button(pw_frame, text=" Clear Fields ", bg="#181818", fg="white", font=("Times 12"), command=self.clear)
        clear_button.pack(side="left", padx=(10, 10))
        
        # vertical seperator
        ttk.Separator(pw_frame, orient='vertical').pack(side='left', fill='y')
        
        # button to save all user input from entry fields
        save_button = tk.Button(pw_frame, text="    Save    ", bg="#181818", fg="white", font=("Times 12"), command=self.save) 
        save_button.pack(side="left", padx=(10, 10))
        
        # vertical seperator
        ttk.Separator(pw_frame, orient='vertical').pack(side='left', fill='y')
        
        # knapscak icon
        myImg = application_path.replace("\\", "/") + "/knapsack.png"
        image1 = Image.open(myImg)
        image1 = image1.resize((80, 40), Image.LANCZOS)
        img = ImageTk.PhotoImage(image1)
        icon_label = tk.Label(pw_frame, image=img, bg=windowColor)
        icon_label.image = img
        icon_label.pack(side="left", padx=(15, 5))
        
        # label - password manager
        pm_label = tk.Label(pw_frame, text="Password\nManager", font="Times 9", fg="white", bg=windowColor)
        pm_label.pack(side="left", padx=0)
        
        # horizontal seperator
        ttk.Separator(seperate_frame, orient='horizontal').pack(side='top', fill='x')
        
        # label displaying the text 'User Name:'
        user_label = tk.Label(user_site, text="User Name: ", bg=windowColor, fg="white", font="Times 12")
        user_label.pack(side="left")
        
        # entry for username
        user_entry = tk.Entry(user_site, textvariable=self.site, width=20, font="Times 12")
        user_entry.pack(side="left")
        
        # label displaying the text 'Site Name:'
        site_label = tk.Label(user_site, text="Site Name: ", bg=windowColor, fg="white", font="Times 12")
        site_label.pack(side="left", padx=(30, 0))
        
        # entry for name of website where the user name and password are stored
        site_entry = tk.Entry(user_site, textvariable=self.user, width=20, font="Times 12")
        site_entry.pack(side="left", padx=(0, 30))
        
        # horizontal seperator
        ttk.Separator(bottom_us, orient='horizontal').pack(side='top', fill='x')
        
        # button to retrieve all of the passwords
        retrieve_button = tk.Button(user_site, text=" Refresh Passwords ", bg="#181818", fg="white", font=("Times 12"), command=self.retrieve) 
        retrieve_button.pack(side="left")
        
        self.retrieve()
        
if __name__ == "__main__":
    app = Passwords()
    app.mainloop()

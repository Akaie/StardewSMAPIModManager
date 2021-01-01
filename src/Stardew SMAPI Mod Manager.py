import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from os import path
import platform
import traceback
import urllib.request
import webbrowser
import ssl

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width = 500, height = 500)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.create_widgets()
        
    def create_widgets(self):
        #Browse Button
        self.browseButton = tk.Button(self)
        self.browseButton["text"] = "Browse..."
        self.browseButton["command"] = self.folderPicker
        self.browseButton.place(x=10, y=10)
        
        #Auto find Steam directory
        self.steamButton = tk.Button(self)
        self.steamButton["text"] = "Steam Location"
        self.steamButton["command"] = self.steamFolderFinder
        self.steamButton.place(x=80,y=10)
        
        #Path to location picked label
        self.pathTo = tk.Label(self, wrap=450)
        self.pathTo["text"] = ""
        self.pathTo.place(x=10, y=40)
        
        #Enabled title label
        self.enabledTitle = tk.Label(self)
        self.enabledTitle["text"] = "Enabled"
        self.enabledTitle.place(x=10, y=80)
        
        #Enabled listbox
        self.enabledscroll = tk.Scrollbar(self, orient="vertical")
        self.enabledList = tk.Listbox(yscrollcommand=self.enabledscroll, selectmode='multiple')
        self.enabledList.place(x=10, y=100, height=380, width=200)
        
        #Disabled title label
        self.disabledTitle = tk.Label(self)
        self.disabledTitle["text"] = "Disabled"
        self.disabledTitle.place(x=280, y=80)
        
        #Disabled listbox
        self.disabledscroll = tk.Scrollbar(self, orient="vertical")
        self.disabledList = tk.Listbox(yscrollcommand=self.disabledscroll, selectmode='multiple')
        self.disabledList.place(x=280, y=100, height=380, width=200)
        
        #toDisabled Button
        self.toDisabled = tk.Button(self)
        self.toDisabled["text"] = ">>"
        self.toDisabled["command"] = self.moveToDisabled
        self.toDisabled.place(x=230, y=250)
        
        #toEnabled Button
        self.toEnabled = tk.Button(self)
        self.toEnabled["text"] = "<<"
        self.toEnabled["command"] = self.moveToEnabled
        self.toEnabled.place(x=230, y=280)
        
        #load location if exists
        try:
            if platform.system() == "Darwin":
                homedir = path.expanduser('~')
                datapath = homedir+"/Library/Application Support/stardewModManagerdata"
            else:
                datapath = "data"
            if path.exists(datapath):
                data = open(datapath)
                self.pathTo["text"] = data.read()
                data.close()
                if not self.pathTo["text"] == "" and path.exists(self.pathTo["text"]):
                    self.populateLists(self.pathTo["text"])
        except Exception as e:
            messagebox.showerror(title=None, message="There was an error. A file has been produced in the location of the program. Please send this to the author and they'll try to get you sorted!")
            error_file = open("error_log.txt", "w")
            error_file.write(traceback.format_exc())
            error_file.close()
        
    def folderPicker(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected == "":
            self.pathTo["text"] = folder_selected
            self.populateLists(folder_selected)
    
    def populateLists(self, loc):
        try:
            if path.exists(loc):
                self.enabledList.delete(0,tk.END)
                self.disabledList.delete(0, tk.END)
                for dirs in next(os.walk(loc))[1]:
                    if(dirs[0:1] != "."):
                        self.enabledList.insert(self.enabledList.size(), dirs)
                    else:
                        self.disabledList.insert(self.enabledList.size(), dirs[1:])
        except Exception as e:
            messagebox.showerror(title=None, message="There was an error. A file has been produced in the location of the program. Please send this to the author and they'll try to get you sorted!")
            error_file = open("error_log.txt", "w")
            error_file.write(traceback.format_exc())
            error_file.close()

    def steamFolderFinder(self):
        try:
            if platform.system() == "Windows":
                if path.exists("C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Mods"):
                    self.pathTo["text"] = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Mods"
                    self.populateLists(self.pathTo["text"])
                if path.exists("C:\Program Files\Steam\steamapps\common\Stardew Valley\Mods"):
                    self.pathTo["text"] = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Mods"
                    self.populateLists(self.pathTo["text"])
            if platform.system() == "Darwin":
                homedir = path.expanduser('~')
                if path.exists(homedir+"/Library/Application Support/Steam/steamapps/common/Stardew Valley/Mods"):
                    self.pathTo["text"] = homedir+"/Library/Application Support/Steam/steamapps/common/Stardew Valley/Mods"
                    self.populateLists(self.pathTo["text"])
        except Exception as e:
            messagebox.showerror(title=None, message="There was an error. A file has been produced in the location of the program. Please send this to the author and they'll try to get you sorted!")
            error_file = open("error_log.txt", "w")
            error_file.write(traceback.format_exc())
            error_file.close()
    def moveToDisabled(self):
        tupleEnabled = self.enabledList.curselection()
        try:
            for i in tupleEnabled:
                holder = self.enabledList.get(i)
                os.rename(self.pathTo["text"] + "/" + holder, self.pathTo["text"] + "/." + holder)
                self.enabledList.delete(i)
                self.disabledList.insert(self.disabledList.size(), holder)
        except Exception as e:
            messagebox.showerror(title=None, message="There was an error. A file has been produced in the location of the program. Please send this to the author and they'll try to get you sorted!")
            error_file = open("error_log.txt", "w")
            error_file.write(traceback.format_exc())
            error_file.close()
                
    def moveToEnabled(self):
        tupleDisabled = self.disabledList.curselection()
        try:
            for i in tupleDisabled:
                holder = self.disabledList.get(i)
                os.rename(self.pathTo["text"] + "/." + holder, self.pathTo["text"] + "/" + holder)
                self.disabledList.delete(i)
                self.enabledList.insert(self.enabledList.size(), holder)
        except Exception as e:
            messagebox.showerror(title=None, message="There was an error. A file has been produced in the location of the program. Please send this to the author and they'll try to get you sorted!")
            error_file = open("error_log.txt", "w")
            error_file.write(traceback.format_exc())
            error_file.close()

        
def closingWindow(app, root):
    try:
        if platform.system() == "Darwin":
            homedir = path.expanduser('~')
            data = open(homedir+"/Library/Application Support/stardewModManagerdata", "w")
        else:
            data = open("data", "w")
        data.write(app.pathTo["text"])
        data.close()
    except Exception as e:
        messagebox.showerror(title=None, message=str(e))
    root.destroy()

root = tk.Tk()
root.title("Stardew Mod Manager")
root.geometry("500x500")
root.resizable(0,0)
root.iconbitmap('3.ico')
app=Application(master=root)
root.protocol("WM_DELETE_WINDOW", lambda: closingWindow(app, root))
updatekey = "e93a683d4db167202baad2b49bfc526912ec0578baaf38ba6914f5d77606adbc"
try:
    messagebox.showinfo("Checking", "Checking for updates!")
    context=ssl._create_unverified_context()
    updatematchurlobject = urllib.request.urlopen("https://raw.githubusercontent.com/Akaie/StardewSMAPIModManager/main/Executables/key", context=context)
    updatematch = updatematchurlobject.read().decode('utf-8')
    if updatekey != updatematch:
        dia = messagebox.askquestion("Update found!", "There appears to be an update! Do you want to go to the Nexus Mod page?")
        if dia == "yes":
            webbrowser.open("https://www.nexusmods.com/stardewvalley/mods/7365")
    else:
        messagebox.showinfo("Checking", "No updates, carry on!")
        
except Exception:
    messagebox.showerror("Checkfailed", "Program was undable to check for updates, is your internet down?")
root.mainloop()

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Menu
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
        #menubar
        menubar = Menu(self)
        loadoutmenu = Menu(menubar, tearoff=0)
        loadoutmenu.add_command(label="Save Loadout...", command = self.loadoutSave)
        loadoutmenu.add_command(label="Load Loadout...", command = self.loadoutLoad)
        menubar.add_cascade(label="File", menu=loadoutmenu)
        self.master.config(menu=menubar)
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

    def loadoutLoad(self):
        locationToLoad = filedialog.askopenfile(filetypes = [(".load Files", "*.load")])
        self.pathTo["text"] = ""
        self.enabledList.delete(0,tk.END)
        self.disabledList.delete(0, tk.END)
        try:
            cancelled = False
            if path.exists(locationToLoad.name):
                with open(locationToLoad.name, "r") as f:
                    line = f.readline()
                    if line:
                        if path.exists(line.strip()):
                            self.pathTo["text"] = line.strip()
                            disabledlisttomonitor = []
                            enabledlisttomonitor = []
                            for dirs in next(os.walk(line.strip()))[1]:
                                if(dirs[0:1] != "."):
                                    enabledlisttomonitor.append(dirs)
                                else:
                                    disabledlisttomonitor.append(dirs)
                        else:
                            messagebox.showerror(message="The folder specified in this .load file no longer exists, can't load this file!")
                            cancelled = True
                    else:
                        messagebox.showerror(message="This file is empty, can't load this file!")
                    line = f.readline()
                    while line and not cancelled:
                        if not line[0:1] == ".":
                            if line.strip() in enabledlisttomonitor:
                                enabledlisttomonitor.remove(line.strip())
                            if "."+line.strip() in disabledlisttomonitor:
                                disabledlisttomonitor.remove("."+line.strip())
                            if path.exists(self.pathTo["text"] + "/"+line.strip()):
                                self.enabledList.insert(self.enabledList.size(), line.strip())
                            elif path.exists(self.pathTo["text"] + "/."+line.strip()):
                                os.rename(self.pathTo["text"] + "/." + line.strip(), self.pathTo["text"] + "/" + line.strip())
                                self.enabledList.insert(self.enabledList.size(), line.strip())
                            else:
                                messagebox.showerror(message=line.strip()+" is not in the mod folder, skipping!")
                        else:
                            if line.strip()[1:] in enabledlisttomonitor:
                                enabledlisttomonitor.remove(line.strip()[1:])
                            if line.strip() in disabledlisttomonitor:
                                disabledlisttomonitor.remove(line.strip())
                            if path.exists(self.pathTo["text"] + "/."+line.strip()[1:]):
                                self.disabledList.insert(self.disabledList.size(), line.strip()[1:])
                            elif path.exists(self.pathTo["text"] + "/"+line.strip()[1:]):
                                os.rename(self.pathTo["text"] + "/" + line.strip()[1:], self.pathTo["text"] + "/." + line.strip()[1:])
                                self.disabledList.insert(self.disabledList.size(), line.strip()[1:])
                            else:
                                messagebox.showerror(message=line.strip()+" is not in the mod folder, skipping!")
                        line = f.readline()
                    f.close()
                    if len(enabledlisttomonitor) != 0 or len(disabledlisttomonitor) != 0:
                        for i in enabledlisttomonitor:
                            self.enabledList.insert(self.enabledList.size(), i)
                        for i in disabledlisttomonitor:
                            self.disabledList.insert(self.disabledList.size(), i)
                        messagebox.showinfo(message="There were mods in your folder not specified in the load folder, these have defaulted to their current state.")
        except IOError as e:
            messagebox.showerror(message = "Couldn't open the file, aborting!\n"+str(e))
    def loadoutSave(self):
        locationToSave = filedialog.asksaveasfilename(filetypes = [(".load Files", "*.load")])
        if not path.exists(path.dirname(locationToSave)):
            try:
                os.makedirs(path.dirname(filename))
            except OSError as e:
                messagebox.showerror(message = "Couldn't create the folder structure to save file in, aborting!\n"+str(e))
        try:
            with open(locationToSave, "w") as f:
                f.write(self.pathTo["text"]+"\n")
                for i in range(0,self.enabledList.size()):
                    f.write(self.enabledList.get(i)+"\n")
                for i in range(0,self.disabledList.size()):
                    f.write("."+self.disabledList.get(i)+"\n")
                f.close()
        except IOError as e:
            messagebox.showerror(message = "Couldn't open the file for saving!\n"+ str(e))
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
            for i in reversed(tupleEnabled):
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
            for i in reversed(tupleDisabled):
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
updatekey = "ee821072f3f8be34269a2091fd24eb0e819175dde52cb923888af6fd09dfb34d"
try:
    messagebox.showinfo("Checking", "Checking for updates!")
    context=ssl._create_unverified_context()
    updatematchurlobject = urllib.request.urlopen("https://raw.githubusercontent.com/Akaie/StardewSMAPIModManager/main/bin/key", context=context)
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

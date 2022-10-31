import os
import platform
import shutil
import ssl
import subprocess
import tkinter as tk
import traceback
import urllib.request
import webbrowser

from os import path
from tkinter import Menu, PhotoImage, filedialog, messagebox, ttk


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, width = 500, height = 500)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        self.create_widgets()

    def create_widgets(self):
        #set up slash for different systems
        if platform.system() == "Darwin" or platform.system() == "Linux":
            self.slash = "/"
        else:
            self.slash = "\\"

        #List of paths in tree
        self.pathlist = []

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
        self.enabledList = ttk.Treeview(yscrollcommand=self.enabledscroll, selectmode='extended', show="tree")
        self.enabledList.place(x=10, y=100, height=380, width=200)
        #self.enabledList.bind("<<ListboxSelect>>", self.selectionChanged)

        #Disabled title label
        self.disabledTitle = tk.Label(self)
        self.disabledTitle["text"] = "Disabled"
        self.disabledTitle.place(x=280, y=80)

        #Disabled listbox
        self.disabledscroll = tk.Scrollbar(self, orient="vertical")
        self.disabledList = ttk.Treeview(yscrollcommand=self.disabledscroll, selectmode='extended', show="tree")
        self.disabledList.place(x=280, y=100, height=380, width=200)
        #self.disabledList.bind("<<ListboxSelect>>", self.selectionChanged)

        self.recentlist = [""]*20
        #load location if exists

        if platform.system() == "Darwin":
            homedir = path.expanduser('~')
            self.datapath = homedir + "/Library/Application Support/stardewModManagerdata"
        else:
            self.datapath = "data"

        try:
            if path.exists(self.datapath):
                data = open(self.datapath)
                count = 0

                for lo in data:
                    if lo.find(":::datapath:::") != -1:
                        self.pathTo["text"] = lo.strip().replace(":::datapath:::", "")
                    else:
                        if count < 10:
                            self.recentlist[count] = lo.strip()
                            count += 1

                data.close()

                if not self.pathTo["text"] == "" and path.exists(self.pathTo["text"]):
                    self.populateLists(self.pathTo["text"])

        except Exception as e:
            log_exception(e)

        self.disHold = None
        self.enHold = None

        #menubar
        self.menubar = Menu(self)
        self.loadoutmenu = Menu(self.menubar, tearoff=0)
        self.recentclicked = ""
        self.recentmenu = Menu(self.loadoutmenu, self.recentclicked, tearoff = 0)

        self.updateRecentMenu()

        self.loadoutmenu.add_command(label="Save Loadout...", command = self.loadoutSave)
        self.loadoutmenu.add_command(label="Load Loadout...", command = lambda: self.loadoutLoad(None))
        self.loadoutmenu.add_cascade(label="Recent Loadouts", menu = self.recentmenu)
        self.menubar.add_cascade(label="File", menu=self.loadoutmenu)
        self.master.config(menu=self.menubar)

        #Browse Button
        self.browseButton = tk.Button(self)
        self.browseButton["text"] = "Browse..."
        self.browseButton["command"] = self.folderPicker
        self.browseButton.place(x=10, y=10)

        #Auto find Steam directory
        self.steamButton = tk.Button(self)
        self.steamButton["text"] = "Steam Location"
        self.steamButton["command"] = self.steamFolderFinder
        self.steamButton.place(x=90,y=10)

        #Open Mod Folder Button
        self.openModsButton = tk.Button(self)
        self.openModsButton["text"] = "Open Directory"
        self.openModsButton["command"] = self.openModsFolder
        self.openModsButton.place(x=205, y=10)

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

        #Selected Mod Label
        self.selectedLabel = tk.Label(self)
        self.selectedLabel["text"] = ""
        self.selectedLabel.place(x=10, y=490)

    def openModsFolder(self):
        if path.exists(self.pathTo["text"]):
            if platform.system() == "Darwin":
                subprocess.call(["open", "-R", self.pathTo["text"]])
            elif platform.system() == "Linux":
                subprocess.call(["xdg-open", self.pathTo["text"]])
            else:
                FILEBROWSER_PATH = os.getenv('WINDIR') + "\\" + 'explorer.exe'
                subprocess.run([FILEBROWSER_PATH, self.pathTo["text"]])

    def selectionChanged(self, event):
        selection = event.widget.curselection()
        if selection:
            lastItem = selection[0]
            if event.widget == self.disabledList and self.disHold:
                for i in selection:
                    if i not in self.disHold:
                        lastItem = i
            if event.widget == self.enabledList and self.enHold:
                for i in selection:
                    if i not in self.enHold:
                        lastItem = i
            self.selectedLabel["text"] = event.widget.get(lastItem)
        self.disHold = self.disabledList.curselection()
        self.enHold = self.enabledList.curselection()

    def loadoutLoad(self, isRecent):
        locationToLoad = None
        if isRecent == None:
            locationToLoad = filedialog.askopenfile(filetypes = [(".load Files", "*.load")])
            fileToLoad = locationToLoad.name
        else:
            fileToLoad = isRecent
            locationToLoad = ""
        if locationToLoad != None:
            self.pathTo["text"] = ""
            try:
                cancelled = False
                if path.exists(fileToLoad):
                    with open(fileToLoad, "r") as f:
                        line = f.readline()
                        if line:
                            if path.exists(line.strip()):
                                self.pathTo["text"] = line.strip()
                            else:
                                messagebox.showerror(message="The folder specified in this .load file no longer exists, can't load this file!")
                                cancelled = True
                        else:
                            messagebox.showerror(message="This file is empty, can't load this file!")
                            cancelled = True
                        line = f.readline()
                        while line and not cancelled:
                            linesplit = line.strip().split(self.slash)
                            linefin = linesplit[len(linesplit) - 1]
                            opposite = ""
                            for l in range(0, len(linesplit) - 1):
                                if opposite == "":
                                    opposite = opposite + linesplit[l]
                                else:
                                    opposite = opposite + self.slash + linesplit[l]
                            if not linefin[0:1] == ".":
                                if opposite == "":
                                    opposite = opposite + "." + linesplit[len(linesplit)-1]
                                else:
                                    opposite = opposite + self.slash + "." + linesplit[len(linesplit)-1]
                                if path.exists(self.pathTo["text"] + self.slash + opposite):
                                    os.rename(self.pathTo["text"] + self.slash + opposite, self.pathTo["text"] + self.slash +line.strip())
                            else:
                                if opposite == "":
                                    opposite = opposite + linesplit[len(linesplit)-1][1:]
                                else:
                                    opposite = opposite + self.slash + linesplit[len(linesplit)-1][1:]
                                if path.exists(self.pathTo["text"] + self.slash + opposite):
                                    os.rename(self.pathTo["text"] + self.slash + opposite, self.pathTo["text"] + self.slash + line.strip())
                            line = f.readline()
                        f.close()
                if fileToLoad not in self.recentlist:
                    for i in range(18, -1, -1):
                        self.recentlist[i+1] = self.recentlist[i]
                    self.recentlist[0] = fileToLoad
                    self.updateRecentMenu()
                self.populateLists(self.pathTo["text"])
            except IOError as e:
                messagebox.showerror(message = "Couldn't open the file, aborting!\n"+str(e))

    def loadoutSave(self):
        locationToSave = filedialog.asksaveasfilename(filetypes = [(".load Files", "*.load")])
        if locationToSave != None:
            if not path.exists(path.dirname(locationToSave)):
                try:
                    os.makedirs(path.dirname(filename))
                except OSError as e:
                    messagebox.showerror(message = "Couldn't create the folder structure to save file in, aborting!\n"+str(e))
            try:
                if not ".load" in locationToSave:
                    locationToSave = locationToSave + ".load"
                with open(locationToSave, "w") as f:
                    f.write(self.pathTo["text"]+"\n")
                    for i in self.pathlist:
                        f.write(i+"\n")

                if locationToSave not in self.recentlist:
                    for i in range(18, -1, -1):
                        self.recentlist[i+1] = self.recentlist[i]
                    self.recentlist[0] = locationToSave
                    self.updateRecentMenu()

            except IOError as e:
                messagebox.showerror(message = "Couldn't open the file for saving!\n"+ str(e))

    def updateRecentMenu(self):
        self.recentmenu.delete(0, 'end')
        if self.recentlist[0] != "":
            self.recentmenu.add_command(label=str(1)+": " + path.basename(self.recentlist[0]), command= lambda: self.loadoutLoad(self.recentlist[0]))
        if self.recentlist[1] != "":
            self.recentmenu.add_command(label=str(2)+": " + path.basename(self.recentlist[1]), command= lambda: self.loadoutLoad(self.recentlist[1]))
        if self.recentlist[2] != "":
            self.recentmenu.add_command(label=str(3)+": " + path.basename(self.recentlist[2]), command= lambda: self.loadoutLoad(self.recentlist[2]))
        if self.recentlist[3] != "":
            self.recentmenu.add_command(label=str(4)+": " + path.basename(self.recentlist[3]), command= lambda: self.loadoutLoad(self.recentlist[3]))
        if self.recentlist[4] != "":
            self.recentmenu.add_command(label=str(5)+": " + path.basename(self.recentlist[4]), command= lambda: self.loadoutLoad(self.recentlist[4]))
        if self.recentlist[5] != "":
            self.recentmenu.add_command(label=str(6)+": " + path.basename(self.recentlist[5]), command= lambda: self.loadoutLoad(self.recentlist[5]))
        if self.recentlist[6] != "":
            self.recentmenu.add_command(label=str(7)+": " + path.basename(self.recentlist[6]), command= lambda: self.loadoutLoad(self.recentlist[6]))
        if self.recentlist[7] != "":
            self.recentmenu.add_command(label=str(8)+": " + path.basename(self.recentlist[7]), command= lambda: self.loadoutLoad(self.recentlist[7]))
        if self.recentlist[8] != "":
            self.recentmenu.add_command(label=str(9)+": " + path.basename(self.recentlist[8]), command= lambda: self.loadoutLoad(self.recentlist[8]))
        if self.recentlist[9] != "":
            self.recentmenu.add_command(label=str(10)+": " + path.basename(self.recentlist[9]), command= lambda: self.loadoutLoad(self.recentlist[9]))
        if self.recentlist[10] != "":
            self.recentmenu.add_command(label=str(11)+": " + path.basename(self.recentlist[10]), command= lambda: self.loadoutLoad(self.recentlist[10]))
        if self.recentlist[11] != "":
            self.recentmenu.add_command(label=str(12)+": " + path.basename(self.recentlist[11]), command= lambda: self.loadoutLoad(self.recentlist[11]))
        if self.recentlist[12] != "":
            self.recentmenu.add_command(label=str(13)+": " + path.basename(self.recentlist[12]), command= lambda: self.loadoutLoad(self.recentlist[12]))
        if self.recentlist[13] != "":
            self.recentmenu.add_command(label=str(14)+": " + path.basename(self.recentlist[13]), command= lambda: self.loadoutLoad(self.recentlist[13]))
        if self.recentlist[14] != "":
            self.recentmenu.add_command(label=str(15)+": " + path.basename(self.recentlist[14]), command= lambda: self.loadoutLoad(self.recentlist[14]))
        if self.recentlist[15] != "":
            self.recentmenu.add_command(label=str(16)+": " + path.basename(self.recentlist[15]), command= lambda: self.loadoutLoad(self.recentlist[15]))
        if self.recentlist[16] != "":
            self.recentmenu.add_command(label=str(17)+": " + path.basename(self.recentlist[16]), command= lambda: self.loadoutLoad(self.recentlist[16]))
        if self.recentlist[17] != "":
            self.recentmenu.add_command(label=str(18)+": " + path.basename(self.recentlist[17]), command= lambda: self.loadoutLoad(self.recentlist[17]))
        if self.recentlist[18] != "":
            self.recentmenu.add_command(label=str(19)+": " + path.basename(self.recentlist[18]), command= lambda: self.loadoutLoad(self.recentlist[18]))
        if self.recentlist[19] != "":
            self.recentmenu.add_command(label=str(20)+": " + path.basename(self.recentlist[19]), command= lambda: self.loadoutLoad(self.recentlist[19]))

    def folderPicker(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected == "":
            self.pathTo["text"] = folder_selected
            self.populateLists(folder_selected)

    def populateLists(self, loc):
        try:
            if path.exists(loc):
                self.enabledList.delete(*self.enabledList.get_children())
                self.disabledList.delete(*self.disabledList.get_children())
                self.pathlist.clear()
                for root, dirs, files in os.walk(loc):
                    slasher = root.replace("/", self.slash)
                    slasher = root.replace("\\", self.slash)
                    if path.exists(slasher+self.slash+"manifest.json"):
                        testforparent = False
                        for j in self.pathlist:
                            if j+self.slash in slasher.replace(loc+self.slash, ""):
                                testforparent = True
                        if not testforparent:
                            self.pathlist.append(slasher.replace(loc+self.slash, ""))
                for i in self.pathlist:
                    splitpath = i.split(self.slash)
                    for j in range(0, len(splitpath)):
                        if not splitpath[len(splitpath) - 1][0:1] == ".":
                            if j == 0:
                                if not self.enabledList.exists(splitpath[j]):
                                    self.enabledList.insert('', 'end', splitpath[j], text=splitpath[0])
                            else:
                                if not self.enabledList.exists(splitpath[j]):
                                    self.enabledList.insert(splitpath[j - 1], 'end', splitpath[j], text=splitpath[j])
                        else:
                            if j == 0:
                                if not self.disabledList.exists(splitpath[j]):
                                    self.disabledList.insert('', 'end', splitpath[j], text=splitpath[0])
                            else:
                                if not self.disabledList.exists(splitpath[j]):
                                    self.disabledList.insert(splitpath[j - 1], 'end', splitpath[j], text=splitpath[j])
        except Exception as e:
            log_exception(e)

    def steamFolderFinder(self):
        try:
            if platform.system() == "Windows":
                if path.exists("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stardew Valley\\Mods"):
                    self.pathTo["text"] = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stardew Valley\\Mods"
                if path.exists("C:\\Program Files\\Steam\\steamapps\\common\\Stardew Valley\\Mods"):
                    self.pathTo["text"] = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stardew Valley\\Mods"

            elif platform.system() == "Darwin":
                homedir = path.expanduser('~')
                if path.exists(homedir+"/Library/Application Support/Steam/steamapps/common/Stardew Valley/Mods"):
                    self.pathTo["text"] = homedir+"/Library/Application Support/Steam/steamapps/common/Stardew Valley/Mods"
                if path.exists("/Library/Application Support/Steam/steamapps/common/Stardew Valley/Mods"):
                    self.pathTo["text"] = "/Library/Application Support/Steam/steamapps/common/Stardew Valley/Mods"

            elif platform.system() == "Linux":
                steam_folder = path.expanduser("~") + ".local/share/Steam/steamapps/common/Stardew Valley/Mods"
                if path.exists(steam_folder):
                    self.pathTo["text"] = steam_folder

            self.populateLists(self.pathTo["text"])

        except Exception as e:
            log_exception(e)

    def moveToDisabled(self):
        tupleEnabled = self.enabledList.selection()
        try:
            for i in tupleEnabled:
                parent = self.enabledList.parent(i)
                fulldir = i
                parentsManaged = []
                while parent != '':
                    fulldir = parent + self.slash +fulldir
                    parent = self.enabledList.parent(parent)
                for j in self.pathlist:
                    if fulldir in j:
                        splitpath = j.split(self.slash)
                        if splitpath[len(splitpath)-1][0:1] != ".":
                            splitpath[len(splitpath)-1] = "." + splitpath[len(splitpath)-1]
                        pathToAdd = ""
                        for k in range(0, len(splitpath)):
                            if k == 0:
                                pathToAdd = splitpath[k]
                            else:
                                pathToAdd = pathToAdd + self.slash + splitpath[k]
                            if k == len(splitpath) - 2:
                                os.makedirs(self.pathTo["text"] + self.slash + pathToAdd, exist_ok = True)
                        if not path.exists(self.pathTo["text"] + self.slash + pathToAdd):
                            os.rename(self.pathTo["text"] + self.slash + j, self.pathTo["text"] + self.slash + pathToAdd)
            self.populateLists(self.pathTo["text"])
        except Exception as e:
            log_exception(e)

    def moveToEnabled(self):
        tupleDisabled = self.disabledList.selection()
        try:
            for i in tupleDisabled:
                parent = self.disabledList.parent(i)
                fulldir = i;
                parentsManaged = []
                while parent != '':
                    fulldir = parent + self.slash +fulldir
                    parent = self.disabledList.parent(parent)
                for j in self.pathlist:
                    if fulldir in j:
                        splitpath = j.split(self.slash)
                        while splitpath[len(splitpath) - 1][0:1] == ".":
                            splitpath[len(splitpath) - 1] = splitpath[len(splitpath) - 1][1:]
                        pathToAdd = ""
                        for k in range(0, len(splitpath)):
                            if k == 0:
                                pathToAdd = splitpath[k]
                            else:
                                pathToAdd = pathToAdd + self.slash + splitpath[k]
                            if k == len(splitpath) - 2:
                                os.makedirs(self.pathTo["text"] + self.slash + pathToAdd, exist_ok = True)
                        if not path.exists(self.pathTo["text"] + self.slash + pathToAdd):
                                os.rename(self.pathTo["text"] + self.slash + j, self.pathTo["text"] + self.slash + pathToAdd)
            self.populateLists(self.pathTo["text"])
        except Exception as e:
            log_exception(e)

def log_exception(_):
        messagebox.showerror(title=None, message="There was an error. A log file has been produced in the location of the program for Windows or your Desktop for Mac and Linux. " +
                                "Please send this to the author and they'll try to get you sorted!")

        if platform.system() == "Darwin" or platform.system() == "Linux":
            log_file_dir = path.expanduser('~') + "/Desktop/error_log.txt"

        else:
            log_file_dir = "error_log.txt"

        with open(log_file_dir, 'w') as error_file:
            error_file.write(traceback.format_exc())

def closingWindow(app, root):
    try:
        with open(app.datapath, "w") as data:
            data.write(":::datapath:::"+app.pathTo["text"])
            for i in app.recentlist:
                if i != "":
                    data.write("\n"+str(i))

    except Exception as e:
        log_exception(e)

    finally:
        root.destroy()

root = tk.Tk()
root.title("Stardew SMAPI Mod Manager")
root.geometry("500x540")
root.resizable(0,0)
app = Application(master=root)

if platform.system() == "Linux":
    root.iconphoto(True, PhotoImage(os.getcwd() + app.slash + '3.xbm'))
else:
    root.iconbitmap(PhotoImage(os.getcwd() + app.slash + '3.ico'))

root.protocol("WM_DELETE_WINDOW", lambda: closingWindow(app, root))
updatekey = "90d4148d4b279419b8d2786ce4d0ebbf8656aa70640e3ebf25371200012f88d2"

try:
    context=ssl._create_unverified_context()
    updatematchurlobject = urllib.request.urlopen("https://raw.githubusercontent.com/Akaie/StardewSMAPIModManager/main/bin/key", context=context)
    updatematch = updatematchurlobject.read().decode('utf-8')

    if updatekey != updatematch:
        dia = messagebox.askquestion("Update found!", "There appears to be an update! Do you want to go to the Nexus Mod page?")
        if dia == "yes":
            webbrowser.open("https://www.nexusmods.com/stardewvalley/mods/7365")

except Exception:
    messagebox.showerror("Checkfailed", "Program was undable to check for updates, is your internet down?")

root.mainloop()

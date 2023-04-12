from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os, sys, subprocess, shutil
import psutil

destIsSet = False
paths = []

# dont take dupes
def get_files():
    inp = filedialog.askopenfilenames()
    for item in inp:
        paths.append(item)
        toDisplay = item[item.rfind("/")+1:]
        filesLb.insert(END, toDisplay)


def remove_files():
    path_list = []
    for item in filesLb.curselection():
        path_list.insert(0, item)
    for item in path_list:
        filesLb.delete(item)


def get_destination():
    dest_path.set(filedialog.askdirectory())


def Error(msg:str):
    err = Toplevel()

    def closeWin():
        err.destroy()

    err.grab_set()
    err.title("Error")
    label = Label(err, bg="black", text=msg, padx=10, pady=10)
    close = Button(err, bg="black",  text="Ok", command=closeWin)
    label.pack(side=LEFT)
    close.pack(side=RIGHT)


def success():
    suc = Toplevel()

    def closeWin():
        win.quit()

    suc.grab_set()
    suc.title("Success")
    label = Label(suc, bg="black", text="Transfer successful", padx=10, pady=10)
    close = Button(suc, bg="black",  text="Ok", command=closeWin)
    label.pack(side=LEFT)
    close.pack(side=RIGHT) 

# Check if file with name already exists and throw error to chose another name
def move():
    #if folderVal == 0:
    if renameVal.get() == 0:
        for file in paths:
            name = file[file.rfind("/"):]
            shutil.move(file, dest_path.get() + name)
    else:
        if prefixVar.get() == "":
            Error("No prefix provided")
        counter = 0
        for file in paths:
            name = prefixVar.get() + str(counter)
            shutil.move(file, dest_path.get() + "/" + name)
            counter += 1
    success()
    # else:
    #     if renameVal.get() == 0:
    #         for file in paths:
    #             name = file[file.rfind("/"):]
    #             shutil.move(file, dest_path.get() + name)
    #     else:
    #         if prefixVar.get() == "":
    #             Error("No prefix provided")
    #         counter = 0
    #         for file in paths:
    #             name = prefixVar.get() + str(counter)
    #             shutil.move(file, dest_path.get() + "/" + name)
    #             counter += 1
    #     success()


def go():
    if filesLb.size() == 0:
        Error("No files selected")
    elif dest_path.get() == "":
        Error("No destination set")
    else:
        # if folderVal == 1:
        #     print(dest_path.get() + "/" + folderName.get())
        # else:
        #     print(dest_path.get())
        # #os.mkdir(dest_path)
        move()




win = Tk()
win.title("ImgHaul")
win.configure(background="black")
#win.iconbitmap("d500.gif")

### Camera Image ###
#cam = Image.open("d500.gif").resize((300,225), Image.Resampling.LANCZOS)
camera = ImageTk.PhotoImage(file="d500.png")
Label(win, image=camera, bg="black").grid(row=0, column=2, sticky=W)

### Quit Button ###
quitButton = Button(win, text="Quit", command=win.quit)
quitButton.grid(row=3, column=3,sticky=E)



### Go Button ###
goButton = Button(win, text="Go", command=go)
goButton.grid(row=3,column=2,sticky=E)


### Files Listbox ###s
filesFrame = LabelFrame(win, text="Files", bg="black", fg="white")
filesLb = Listbox(filesFrame, width=30, height=20, selectmode=MULTIPLE, relief="sunken", bd=1)
filesLb.pack(side=TOP)
# Directory Button #
dirButton = Button(filesFrame, text="Browse", command=get_files)
dirButton.pack(side=LEFT)
### Remove Button ###
removeButton = Button(filesFrame, text="Remove Files", command=remove_files)
removeButton.pack(side=RIGHT)
filesFrame.grid(row=0, column=0, padx=10, pady=10)



### Destination Settings ###
Destination = LabelFrame(win, width=40, text="Destination", bg="black")

dest_path = StringVar(Destination, value="")
destInp = Label(Destination, textvariable=dest_path, relief=RAISED, bg="black", width=20)
destBrowse = Button(Destination, text="Browse", command=get_destination)
destInp.pack(side=LEFT)
destBrowse.pack(side=RIGHT)
Destination.grid(row=2, column=0, sticky=W)

### New Folder Settings ###
NewFolder = LabelFrame(win, width=40, text="New Folder", bg="black")
folderVal = IntVar()
folderCB = Checkbutton(NewFolder, variable=folderVal, text="Make New Folder", bg="black")
folderName = StringVar(NewFolder, value="New Folder")
folderE = Entry(NewFolder, textvariable=folderName)
folderE.pack(side=BOTTOM)
folderCB.pack(side=LEFT)
NewFolder.grid(row=2, column=1, sticky=W)

### Rename Settings ###
renameFrame = LabelFrame(win, text="Rename", bg="black")
renameVal = IntVar()
prefixVar = StringVar()
renameCB = Checkbutton(renameFrame, bg="black", text="Rename Files", variable=renameVal)
prefix = Entry(renameFrame, textvariable=prefixVar)
prefixLabel = Label(renameFrame, bg="black", text="Select a prefix")
renameCB.pack(side=TOP)
prefix.pack(side=LEFT)
prefixLabel.pack(side=RIGHT)
renameFrame.grid(row=2, column=2, padx=20, sticky=W)


win.mainloop()
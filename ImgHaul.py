#TODO: Add copy as lightweight JPEG frame
#TODO: Check input validation


from tkinter import *
from tkinter import filedialog
from PIL import Image
import shutil, os, exifread, time
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

destIsSet = False
paths = []


def get_files():
    inp = filedialog.askopenfilenames()
    for item in inp:
        if item not in paths:
            paths.append(item)
            toDisplay = item
            filesLb.insert(END, toDisplay)
    genPyplot()


def remove_files():
    path_list = []
    for item in filesLb.curselection():
        path_list.insert(0, item)
    for item in path_list:
        filesLb.delete(item)
        paths.pop(item)
    genPyplot()



def get_destination():
    dest_path.set(filedialog.askdirectory())


def Error(msg:str, win:Tk):
    err = Toplevel()
    def closeWin():
        err.destroy()
        win.quit()
        return
    err.grab_set()
    err.title("Error")
    label = Label(err, bg="gray", text=msg, padx=10, pady=10)
    close = Button(err, bg="gray",  text="Ok", command=closeWin)
    label.pack(side=LEFT)
    close.pack(side=RIGHT)
    err.wait_window()


def success():
    suc = Toplevel()
    def closeWin():
        win.quit()
    suc.grab_set()
    suc.title("Success")
    label = Label(suc, bg="gray", text="Transfer successful", padx=10, pady=10)
    close = Button(suc, bg="gray",  text="Ok", command=closeWin)
    label.pack(side=LEFT)
    close.pack(side=RIGHT) 


def genPyplot():
    fig = Figure(figsize = (6,4))
    mm = {}

    for file in paths:
        f = open(file, 'rb')
        tags = exifread.process_file(f)
        if len(tags) == 0:
            break
        elif int(str(tags["EXIF FocalLength"])) not in mm.keys():
            mm[int(str(tags["EXIF FocalLength"]))] = 1
        else:
            mm[int(str(tags["EXIF FocalLength"]))] += 1

    plot = fig.add_subplot(111)

    xticks = list(sorted(mm.keys()))
    plot.bar(mm.keys(), mm.values())
    plot.set_xticks(xticks)
    plot.set_xticklabels(xticks)

    plot.set_xlabel("Focal Length in mm", fontsize=12)
    plot.set_ylabel("Occurrences", fontsize=12)
    plot.set_title("Focal Length Distribution", fontsize=16)

    if not mm:
        plot.set_yticks([1])
    else:
        plot.yaxis.set_major_locator(MaxNLocator(integer=True))

    frame = Frame(win)
    canvas = FigureCanvasTkAgg(fig,master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    frame.grid(row=0, column=1, pady=10, sticky=W)

# Check if file with name already exists and throw error to chose another name
def move(win):
    if jpegVal.get() == 0:
        # If not renaming 
        if renameVal.get() == 0:
            # Get filename from each path, move it to destination path
            for file in paths:
                name = file[file.rfind("/"):]
                shutil.move(file, dest_path.get() + name)
        # If renaming
        else:
            # Check for empty prefix
            if prefixVar.get() == "":
                Error("No prefix provided", win)
                win.destroy()
            counter = 0
            # Check for illegal characters, then move
            for file in paths:
                illegalCh = ["#", "%", "&", "{", "}", "/", "<", ">", ".", "\\", "[", "]", ":", ";", "|", ","]
                for ch in illegalCh:
                    if prefixVar.get().find(ch) != -1:
                        Error("Illegal character " + ch + " in prefix", win)
                        return
                name = prefixVar.get() + "_" + str(counter) + file[file.rfind("."):]
                shutil.move(file, dest_path.get() + "/" + name)
                counter += 1
        success()
    else:
        # If not renaming
        if renameVal.get() == 0:
            for file in paths:
                newPath = dest_path.get() + "/" + file[file.rfind("/"):]
                newPath = newPath[:newPath.rfind(".")] + ".jpg"
                img = Image.open(file)
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(newPath, format="JPEG", quality=quality.get(), subsampling=0)
        # If renaming
        else:
            if prefixVar.get() == "":
                Error("No prefix provided", win)
                win.destroy()
            counter = 0
            # Check for illegal characters, then move
            for file in paths:
                illegalCh = ["#", "%", "&", "{", "}", "/", "<", ">", ".", "\\", "[", "]", ":", ";", "|", ","]
                for ch in illegalCh:
                    if prefixVar.get().find(ch) != -1:
                        Error("Illegal character " + ch + " in prefix", win)
                        return
                newPath = dest_path.get() + "/" + prefixVar.get() + "_" + str(counter) + file[file.rfind("."):]
                newPath = newPath[:newPath.rfind(".")] + ".jpg"
                img = Image.open(file)
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(newPath, format="JPEG", quality=quality.get(), subsampling=0)
                counter += 1
        success()



def go(win):
    if filesLb.size() == 0:
        Error("No files selected", win)
        win.destroy()
    elif dest_path.get() == "":
        Error("No destination set", win)
        win.destroy()
    else:
        if folderVal.get() == 1:
            illegalCh = ["#", "%", "&", "{", "}", "/", "<", ">", ".", "\\", "[", "]", ":", ";", "|", ","]
            dir = folderName.get()
            for ch in illegalCh:
                if folderName.get().find(ch) != -1:
                    Error("Illegal character " + ch + " in folder name", win)
                    return
            parentDir = dest_path.get()
            path = os.path.join(parentDir, dir)
            if (os.path.exists(path)):
                Error("Path already exists", win)
                return
            os.mkdir(path)
            dest_path.set(path)
        move(win)



win = Tk()
win.title("ImgHaul")
win.configure(background="gray")
win.resizable(False, False)

### Quit Button ###
quitButton = Button(win, text="Quit", command=win.quit)
quitButton.grid(row=3, column=3,sticky=E)
### Go Button ###
goButton = Button(win, text="Go", command=lambda: go(win))
goButton.grid(row=3,column=2,sticky=E)


### Files Listbox ###s
filesFrame = LabelFrame(win, text="Files", bg="gray")
filesLb = Listbox(filesFrame, width=30, height=20, selectmode=MULTIPLE, bg="dark gray", relief="sunken", bd=1)
filesLb.pack(side=TOP)
# Directory Button #
dirButton = Button(filesFrame, text="Browse", command=get_files)
dirButton.pack(side=LEFT)
# Remove Button #
removeButton = Button(filesFrame, text="Remove Files", command=remove_files)
removeButton.pack(side=RIGHT)
filesFrame.grid(row=0, column=0, padx=10)


### Destination Settings ###
Destination = LabelFrame(win, width=40, text="Destination", bg="gray")
dest_path = StringVar(Destination, value="")
destInp = Label(Destination, textvariable=dest_path, relief=RAISED, bg="gray", width=20)
destBrowse = Button(Destination, text="Browse", command=get_destination)
# New Folder Settings #
folderVal = IntVar()
folderCB = Checkbutton(Destination, variable=folderVal, text="Make New Folder", bg="gray")
folderName = StringVar(Destination, value="New Folder")
folderE = Entry(Destination, textvariable=folderName)
folderE.pack(side=BOTTOM)
folderCB.pack(side=BOTTOM)
destInp.pack(side=LEFT)
destBrowse.pack(side=RIGHT)
Destination.grid(row=2, column=0, padx=10, sticky=W)

### Rename Settings ###
renameFrame = LabelFrame(win, text="Rename", bg="gray")
renameVal = IntVar()
prefixVar = StringVar()
renameCB = Checkbutton(renameFrame, bg="gray", text="Rename Files", variable=renameVal)
prefix = Entry(renameFrame, textvariable=prefixVar)
prefixLabel = Label(renameFrame, bg="gray", text="Select a prefix")
renameCB.pack(side=TOP)
prefix.pack(side=LEFT)
prefixLabel.pack(side=RIGHT)
renameFrame.grid(row=2, column=1, padx=(140,0), sticky=W)

### Copy as JPEG ###
jpegFrame = LabelFrame(win, text="Copy as JPEG", bg="gray")
quality = IntVar()
jpegVal = IntVar()
asJpeg = Checkbutton(jpegFrame, bg="gray", text="Copy files as JPEGs", variable=jpegVal)
qualLabel = Label(jpegFrame, bg="gray", text="Quality")
qualSlider = Scale(jpegFrame, bg="gray", orient= HORIZONTAL, variable=quality, from_=1,to=100)
asJpeg.pack(side=TOP)
qualLabel.pack(side=BOTTOM)
qualSlider.pack(side=BOTTOM)
jpegFrame.grid(row=2, column=2)

genPyplot()

win.mainloop()
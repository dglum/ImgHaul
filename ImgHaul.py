#TODO: optimize exif so it's not slow

import piexif
from tkinter import *
from tkinter import filedialog
from PIL import Image, ExifTags
import shutil, os, exifread
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


def folderLockToggle():
    if folderEState.get() == "disabled":
        folderE.config(state="normal")
        folderEState.set("normal")
    else:
        folderE.delete(0, END)
        folderE.insert(0, "New Folder")
        folderE.config(state="disabled")
        folderEState.set("disabled")
        

def renameLockToggle():
    if prefixState.get() == "disabled":
        prefix.config(state="normal")
        prefixState.set("normal")
    else:
        prefix.delete(0, END)
        prefix.insert(0, "Select a prefix")
        prefix.config(state="disabled")
        prefixState.set("disabled")


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
    fig.set_facecolor("gray")
    mm = {} 

    for file in paths:
        #f = open(file, 'rb')
        data = piexif.load(file)
        if piexif.ExifIFD.FocalLength in data:
            print("YES")
            continue
        else:
            print("n")
            continue
        
        tags = exifread.process_file(f, stop_tag='EXIF FocalLength')
        if len(tags) == 0:
            continue
        # if len(tags) == 0:
        #     break
        # elif int(str(tags["EXIF FocalLength"])) not in mm.keys():
        #     mm[int(str(tags["EXIF FocalLength"]))] = 1
        # else:
        #     mm[int(str(tags["EXIF FocalLength"]))] += 1
        focalLength = tags.get("EXIF FocalLength")
        focalLength = str(focalLength)
        print(focalLength)
        if focalLength is not None:
            if "/" in focalLength:
                num, denom = focalLength.split("/")
                focalLength = float(num) / float(denom)
            else:
                focalLength = int(focalLength)
            if focalLength not in mm.keys():
                mm[focalLength] = 1
            else:
                mm[focalLength] += 1

    plot = fig.add_subplot(111)
    #print(type(list(mm.keys())[0]))
    
    xticks = list(sorted(mm.keys()))
    plot.bar(mm.keys(), mm.values(), color="white")
    plot.set_xticks(xticks)
    plot.set_xticklabels(xticks)
    plot.tick_params(colors="white")

    plot.set_xlabel("Focal Length in mm", fontsize=12, color="white")
    plot.set_ylabel("Occurrences", fontsize=12, color="white")
    plot.set_title("Focal Length Distribution", fontsize=16, color="white")
    plot.spines[:].set_color("white")
    plot.set_facecolor("gray")

    if not mm:
        plot.set_yticks([1])
    else:
        plot.yaxis.set_major_locator(MaxNLocator(integer=True))

    frame = Frame(win,border=3,relief=GROOVE)
    canvas = FigureCanvasTkAgg(fig,master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    frame.grid(row=0, column=0, padx=(300,15) ,pady=10, sticky=W)

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


##### Main Frame #####
mf = Frame(win, bg="gray")


### Files Listbox ###s
filesFrame = LabelFrame(win, text="Files", bg="gray")
filesLb = Listbox(filesFrame, width=30, height=20, selectmode=MULTIPLE, bg="dark gray", relief="sunken", bd=1)
filesLb.pack(side=TOP)
# Directory Button #
dirButton = Button(filesFrame, text="Browse", highlightbackground="gray", highlightcolor="gray", command=get_files)
dirButton.pack(side=LEFT)
# Remove Button #
removeButton = Button(filesFrame, text="Remove Files", highlightbackground="gray", highlightcolor="gray", command=remove_files)
removeButton.pack(side=RIGHT)
filesFrame.grid(row=0, column=0, padx=10, sticky=W)


### Destination Settings ###
Destination = LabelFrame(mf, width=40, text="Destination", bg="gray")
dest_path = StringVar(Destination, value="")
destInp = Label(Destination, textvariable=dest_path, width=20)
destBrowse = Button(Destination, text="Browse", highlightbackground="gray", highlightcolor="gray", command=get_destination)
# New Folder Settings #
folderVal = IntVar()
folderCB = Checkbutton(Destination, variable=folderVal, text="Make New Folder", bg="gray", command=folderLockToggle)
folderName = StringVar(Destination, value="New Folder")
folderEState = StringVar()
folderEState.set("disabled")
folderE = Entry(Destination, highlightbackground="gray", highlightcolor="gray", state="disabled", textvariable=folderName)
folderE.pack(side=BOTTOM)
folderCB.pack(side=BOTTOM)
destInp.pack(side=LEFT)
destBrowse.pack(side=RIGHT)
Destination.grid(row=0, column=0)

### Rename Settings ###
renameFrame = LabelFrame(mf, text="Rename", bg="gray")
renameVal = IntVar()
prefixVar = StringVar()
prefixVar.set("Select a prefix")
renameCB = Checkbutton(renameFrame, bg="gray", text="Rename Files", variable=renameVal, command=renameLockToggle)
prefixState = StringVar()
prefixState.set("disabled")
prefix = Entry(renameFrame, highlightbackground="gray", highlightcolor="gray", state="disabled", textvariable=prefixVar)
renameCB.pack(side=TOP)
prefix.pack(side=LEFT)
renameFrame.grid(row=0, column=1, padx=10)

### Copy as JPEG ###
jpegFrame = LabelFrame(mf, text="Copy as JPEG", bg="gray")
quality = IntVar()
jpegVal = IntVar()
asJpeg = Checkbutton(jpegFrame, bg="gray", text="Copy files as JPEGs", variable=jpegVal)
qualLabel = Label(jpegFrame, bg="gray", text="Quality")
qualSlider = Scale(jpegFrame, bg="gray", orient= HORIZONTAL, variable=quality, from_=1,to=100)
asJpeg.pack(side=TOP)
qualLabel.pack(side=BOTTOM)
qualSlider.pack(side=BOTTOM)
jpegFrame.grid(row=0, column=2)

### Go Button ###
goButton = Button(mf, text="Go", highlightbackground="gray", highlightcolor="gray", command=lambda: go(win))
goButton.grid(row=0,column=3, padx=(80,0), sticky=N, pady=(30,0))

### Quit Button ###
quitButton = Button(mf, text="Quit", highlightbackground="gray", highlightcolor="gray", command=win.quit)
quitButton.grid(row=0, column=3, pady=(50,5), padx=(80,0))



mf.grid(row=1, column=0, pady=(0,10))

genPyplot()

win.mainloop()
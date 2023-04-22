#TODO: What's going on with New Folder
#TODO: Move New Folder into Destination frame
#TODO: Add copy as lightweight JPEG frame
#TODO: Input validation maybe?


from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import shutil
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import exifread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

destIsSet = False
paths = []


def get_files():
    inp = filedialog.askopenfilenames()
    for item in inp:
        if item not in paths:
            paths.append(item)
            toDisplay = item#[item.rfind("/")+1:]
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
    #if folderVal == 0:
    if renameVal.get() == 0:
        for file in paths:
            name = file[file.rfind("/"):]
            shutil.move(file, dest_path.get() + name)
    else:
        if prefixVar.get() == "":
            Error("No prefix provided", win)
            win.destroy()
            #sys.exit()
        counter = 0
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


def go(win):
    if filesLb.size() == 0:
        Error("No files selected", win)
        win.destroy()
    elif dest_path.get() == "":
        Error("No destination set", win)
        win.destroy()
    else:
        # if folderVal == 1:
        #     print(dest_path.get() + "/" + folderName.get())
        # else:
        #     print(dest_path.get())
        # #os.mkdir(dest_path)
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
destInp.pack(side=LEFT)
destBrowse.pack(side=RIGHT)
Destination.grid(row=2, column=0, padx=10, sticky=W)

### New Folder Settings ###
NewFolder = LabelFrame(win, width=40, text="New Folder", bg="gray")
folderVal = IntVar()
folderCB = Checkbutton(NewFolder, variable=folderVal, text="Make New Folder", bg="gray")
folderName = StringVar(NewFolder, value="New Folder")
folderE = Entry(NewFolder, textvariable=folderName)
folderE.pack(side=BOTTOM)
folderCB.pack(side=LEFT)
NewFolder.grid(row=2, column=1, sticky=W)

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

genPyplot()

win.mainloop()
import reapy
from reapy import reascript_api as RPR
Project = reapy.Project()

import difflib
import whisper
model = whisper.load_model("small.en")


def get_media_source_filename(item):

    item_take = item.active_take
    Item_source = item_take.source
    filename = Item_source.filename

    return filename

def Transcribe_audio(Path):

    result = model.transcribe(Path)

    printtext = (result["text"])

    return printtext

def Get_and_process_audio():
    
    if not 'csvfile' in globals():
        Errormessege()
        
    if getnamesfromcsv.get() == False:
        namelist = []

    N_items = Project.n_selected_items

    itemnum = 0

    for _ in range(N_items):

        sel_item = Project.get_selected_item(itemnum)
        filename = get_media_source_filename(sel_item)
        text = Transcribe_audio(filename)

        itempos = sel_item.get_info_value("D_POSITION")
        itemlen = sel_item.get_info_value("D_LENGTH")
        itemend = itempos + itemlen
        
        Project.add_marker(itempos, text)
        
        if getnamesfromcsv.get() == True:
            regname = ParseCsv(text)
            Project.add_region(itempos, itemend, regname, color=0)
            inserttext(regname,text)
        else:
            inserttext(str(itemnum),text)
            addtolist = str(itemnum) + ',' + text
            namelist.append(addtolist)

        itemnum = itemnum + 1

    if getnamesfromcsv.get() == False:
        with open(asksaveasfilename(filetypes=[("CSV files", "*.csv")]), 'w') as csv:
            for items in namelist:
                csv.write("%s\n" % items)

    itemnum = 0



def Getcsv():
    global csvfile
    csvfile = askopenfilename(filetypes=[("CSV files", "*.csv")])
    


def ParseCsv(word):
    with open(csvfile, 'r') as csv_file:
        
        match = difflib.get_close_matches(word, csv_file, n=1, cutoff=0.4)
        
        litostring = ''.join(match)
        linename = litostring.split(',')

        return (linename[0])



def center_window(rootwindow ,width=300, height=200):
    # get screen width and height
    screen_width = rootwindow.winfo_screenwidth()
    screen_height = rootwindow.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    rootwindow.geometry('%dx%d+%d+%d' % (width, height, x, y))



def SetSettings():
    secondary_window = Toplevel(root)
    secondary_window.title("Secondary Window")
    secondary_window.config(width=300, height=200)
    button_close = ttk.Button(
        secondary_window,
        text="Close window",
        command=secondary_window.destroy
    )
    button_close.place(x=100, y=100)



def Errormessege():
    Errormessege_window = Toplevel(root)
    Errormessege_window.resizable(False, False)
    Errormessege_window.title("Error")
    Errormessege_window.config(width=300, height=100)
    center_window(Errormessege_window,300,100)
    Errortext = ttk.Label( 
        Errormessege_window,
        text="No CSV file do you want to load one?",
        anchor="center",
        justify="center"
    )
    Errortext.pack(side=TOP,ipadx=40,ipady=10,expand=True)

    buttonerror_yes = ttk.Button(
        Errormessege_window,
        text="yes",
        command=lambda:[Getcsv(), Errormessege_window.destroy()]
    )

    buttonerror_yes.pack(side=LEFT,ipadx=10,ipady=3,padx=8,pady=8,expand=True)

    buttonerror_no = ttk.Button(
        Errormessege_window,
        text="no",
        command=lambda:[getnamesfromcsv.set(False), Errormessege_window.destroy()]
    )

    buttonerror_no.pack(side=RIGHT,ipadx=10,ipady=3,padx=8,pady=8,expand=True)




from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

import uuid
import sv_ttk

root = Tk(className='rea-speech to text')
root.geometry("600x400")
root.resizable(False, False)


scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")

        # Treeview
treeview = ttk.Treeview(
    root,
    selectmode="browse",
    yscrollcommand=scrollbar.set,
    columns=(1),
    height=14,
)

treeview.pack(expand=True, fill="both")
scrollbar.config(command=treeview.yview)

treeview.column("#0", anchor="w", width=100)
treeview.column(1, anchor="w", width=430)


treeview.heading("#0", text="Name", anchor="center")
treeview.heading(1, text="Text", anchor="center")

setup_button = ttk.Button(root, text="⚙️", command=SetSettings)
setup_button.pack(side=LEFT,ipadx=2,ipady=3,padx=8,expand=False)

getcsv_button = ttk.Button(root, text="CSV", command=Getcsv)
getcsv_button.pack(side=LEFT,ipadx=2,ipady=3,expand=False)

getnamesfromcsv = BooleanVar(root, True)
checkbox = ttk.Checkbutton(root, variable=getnamesfromcsv, onvalue=True, offvalue=False, text="Get names from CSV")
checkbox.pack(side=LEFT,ipadx=2,ipady=3,expand=True)

run_button = ttk.Button(root, text="RUN", command=Get_and_process_audio)
run_button.pack(side=BOTTOM,ipadx=2,ipady=3,expand=True)



def inserttext(linenum, txt):
    linenum = (linenum,)
    txt = (txt,)
    unique_id = uuid.uuid4()
    treeview.insert('', 'end', iid=str(unique_id), text=linenum, values=txt)


sv_ttk.set_theme("dark")
center_window(root,600,400)
root.mainloop()
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os

root = tk.Tk()
root.iconbitmap('icon.ico')
root.title('Maru3D : OBJ To LUA Array Converter')
root.resizable(False, False)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

#Files variables

objsequence=[]
objs = []
mtls = []

#Converter Variables

material = ''

#Set widgets font

s = ttk.Style()
s.configure('.', font=('Arial', 11))

#CheckBoxes variables

CheckVerticies = tk.IntVar()
CheckFaces = tk.IntVar()
CheckNormals = tk.IntVar()
CheckTextureCoords = tk.IntVar()
CheckMaterials = tk.IntVar()

version = 'Maru3D OTLA ' + 'v0.5'

OBJSequenceerrortext= 'No OBJ Sequence Folder Loaded'
OBJerrortext= 'No OBJ File Loaded'
MTLerrortext= 'No MTL File Loaded'

errorReason = ''

#Buttons make me go  Y E S
#I suck at python lolololololololol
def makeConsoleText(txt):
    print(txt)
    ConsoleText = tk.Label(scrollable_frame, text=txt, anchor='w')
    ConsoleText.pack(fill='both')

def clearWidgets(directory):
        for widget in directory.winfo_children():
            widget.destroy()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

def addObjSequence():

    clearWidgets(directoryOBJSequenceFrame)

    objsequence.clear()
    filename =filedialog.askdirectory(initialdir="/", title="Select OBJ Sequence Frames Folder")
    #filetypes=((".obj", "*.obj"), (".txt", "*.txt"),("all files", "*.*")))
    if filename == "":
        objsequence.append(OBJSequenceerrortext)
    else:
        objsequence.append(filename)

    print(objsequence)

    defaultOBJSequencetext = tk.Label(directoryOBJSequenceFrame, text=objsequence, bg="#ffffff")
    defaultOBJSequencetext.pack(side=tk.LEFT, fill='both')

def addObj():
    
    clearWidgets(directoryOBJFrame)

    objs.clear()
    filename =filedialog.askopenfilename(initialdir="/", title="Select 3D Model", 
    filetypes=((".obj", "*.obj"), (".txt", "*.txt"),("all files", "*.*")))
    if filename == "":
        objs.append(OBJerrortext)
    else:
        objs.append(filename)

    print(objs)

    defaultOBJtext = tk.Label(directoryOBJFrame, text=objs, bg="#ffffff")
    defaultOBJtext.pack(side=tk.LEFT, fill='both')

def addMtl():

    clearWidgets(directoryMTLFrame)

    mtls.clear()
    filename =filedialog.askopenfilename(initialdir="/", title="Select MTL", 
    filetypes=((".mtl", "*.mtl"), (".txt", "*.txt"),("all files", "*.*")))
    if filename == "":
        mtls.append(MTLerrortext)
    else:
        mtls.append(filename)    

    defaultMTLtext = tk.Label(directoryMTLFrame, text=mtls, bg="#ffffff")
    defaultMTLtext.pack(side=tk.LEFT, fill='both')

    print(mtls)

def convertOBJcode(path, object, exportPlace, errorReason, isSequence):
        if os.path.isfile(path):
                name, extension = os.path.splitext(object)

                if not isSequence:
                    name = 'model'

                if extension == ".obj" or extension == ".txt":

                    folderobjframe = path
                    print(folderobjframe)

                    with open(folderobjframe) as f:
                        lines = f.readlines()

                    dir = "export/"+ exportPlace
                    if not os.path.exists(dir):
                        os.mkdir(dir)

                    with open(dir+name+'.lua', 'w') as exporttext:
                        exporttext.write("--Converted using "+version+"\n\n")

                        if CheckMaterials.get() == 1:
                            exporttext.write("local usematerials = true\n")
                        else:
                            exporttext.write("local usematerials = false\n")

                        exporttext.write("local vertices = {}\n")
                        exporttext.write("local faces = {}\n")
                        exporttext.write("local normals = {}\n")
                        exporttext.write("local texturecoords = {}\n\n")

                        #Get Verticies Code
                        if CheckVerticies.get() == 1:
                            exporttext.write("vertices = {\n")
                            for line in lines:
                                if line.startswith("v "):
                                    finalline = line.lstrip("v ")
                                    finalline = finalline.rstrip()
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == (" "):
                                            exporttext.write(",")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},\n")
                            exporttext.write("};\n")
                
                        #Get Faces Code
                        if CheckFaces.get() == 1 :
                            exporttext.write("faces = {\n")
                            for line in lines:

                                if CheckMaterials.get() == 1:
                                    if line.startswith("usemtl "):
                                        material = line.lstrip("usemtl ")
                                        material = material.rstrip()
        
                                if line.startswith("f "):
                                    finalline = line.lstrip("f ")
                                    finalline = finalline.rstrip()
                                    finalline = finalline.replace('//','/')
                                    exporttext.write("{")
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == ("/"):
                                            exporttext.write(",")
                                        elif char == (" "):
                                            exporttext.write("}, {")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},")
        
                                    if CheckMaterials.get() == 1:
                                        exporttext.write('{"'+material+'"},')
                            
                                    exporttext.write("},\n")
                            exporttext.write("};\n")

                        #Get Normals Code
                        if CheckNormals.get() == 1:
                            exporttext.write("normals = {\n")
                            for line in lines:
                                if line.startswith("vn "):
                                    finalline = line.lstrip("vn ")
                                    finalline = finalline.rstrip()
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == (" "):
                                            exporttext.write(",")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},\n")
                            exporttext.write("};\n")

                        #Get Texture Coords Code
                        if CheckTextureCoords.get() == 1:
                            exporttext.write("texturecoords = {\n")
                            for line in lines:
                                if line.startswith("vt "):
                                    finalline = line.lstrip("vt ")
                                    finalline = finalline.rstrip()
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == (" "):
                                           exporttext.write(",")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},\n")
                            exporttext.write("};\n")

                        exporttext.write("\nreturn {vertices, faces, normals, texturecoords, usematerials};")

                    makeConsoleText("OBJ export finished as "+name+".lua")
                    makeConsoleText("In "+ dir+name+'.lua')
                else:
                    messagebox.showerror('Error', 'Error: ' + 'Incorrect file type\nOnly OBJ and TXT files are allowed')
        else:
            messagebox.showerror('Error', 'Error: ' + errorReason)

def convertObjSequence():
    for sequence in objsequence:
        if os.path.isdir(sequence):
            for path in os.listdir(sequence):
                daPath = os.path.join(sequence, path)
                daObject = path
                name, extension = os.path.splitext(daObject)
                if extension == '.obj' or extension == '.txt':
                    convertOBJcode(daPath, daObject, 'frames/', OBJSequenceerrortext, True)
        else:
            messagebox.showerror('Error', 'Error: ' + OBJSequenceerrortext)

def convertObj():

    for obj in objs:
        objFolder = os.path.basename(obj)
        objFolder = os.path.splitext(objFolder)[0]
        objFile = os.path.splitext(obj)
        objFile = objFolder+objFile[1]
        name, extension = os.path.splitext(objFile)
        convertOBJcode(obj, objFile, name+'/', OBJerrortext, False)

def convertMtl():
    for mtl in mtls:
        if mtls[0] == MTLerrortext:
            errorReason = MTLerrortext
            messagebox.showerror('Error', 'Error: ' + errorReason)
        else:
            with open(mtl) as f:
                    lines = f.readlines()

            file_dir_name = os.path.basename(mtl)
            file_dir_name = os.path.splitext(file_dir_name)[0]

            dir = "export/"+file_dir_name
            if not os.path.exists(dir):
                os.mkdir(dir)

            with open(dir+'/materials.lua', 'w') as exporttext:
                exporttext.write("--Converted using "+version+"\n\n")

                exporttext.write("local materials = {}\n")
                exporttext.write("\nmaterials = {\n")

                for line in lines:
                
                    if line.startswith("newmtl "):
                        finalline = line.lstrip("newmtl ")
                        finalline = finalline.rstrip()
                        exporttext.write('{"'+finalline+'",{')

                    if line.startswith("Kd "):
                        finalline = line.lstrip("Kd ")
                        finalline = finalline.rstrip()
                        for char in finalline:
                            if char == (" "):
                                exporttext.write(",")
                            else:
                                exporttext.write(char)
                        exporttext.write("},},\n")

                exporttext.write("};")
                exporttext.write("\nreturn {materials,};")
                makeConsoleText("MTL export finished as "+"materials.lua")

#Create Frames, Buttons n shit

canvas = tk.Canvas(root, height = 600, width=800, bg="#828282")
canvas.pack()

directoryOBJSequenceFrame = tk.Frame(root, bg="#bdbdbd")
directoryOBJSequenceFrame.place(relwidth=0.5, relheight=0.07, x=30, y=40)

buttonOBJSequenceFrame = tk.Frame(root, bg="#bdbdbd")
buttonOBJSequenceFrame.place(relwidth=0.2, relheight=0.07, x=450, y=40)

directoryOBJFrame = tk.Frame(root, bg="#bdbdbd")
directoryOBJFrame.place(relwidth=0.5, relheight=0.07, x=30, y=100)

buttonOBJFrame = tk.Frame(root, bg="#bdbdbd")
buttonOBJFrame.place(relwidth=0.2, relheight=0.07, x=450, y=100)

directoryMTLFrame = tk.Frame(root, bg="#bdbdbd")
directoryMTLFrame.place(relwidth=0.5, relheight=0.07, x=30, y=160)

buttonMTLFrame = tk.Frame(root, bg="#bdbdbd")
buttonMTLFrame.place(relwidth=0.2, relheight=0.07, x=450, y=160)

frame = tk.Frame(root, bg="#bdbdbd")
frame.place(relwidth=0.5, relheight=0.4, x=30, y=235)

framemtl = tk.Frame(root, bg="#bdbdbd")
framemtl.place(relwidth=0.40, relheight=0.576, x=450, y=235)

#Export Buttons Frames
exportOBJSequencebuttonFrame = tk.Frame(root, bg="#bdbdbd")
exportOBJSequencebuttonFrame.place(relwidth=0.16, relheight=0.121, x=30, y=510)

exportOBJbuttonFrame = tk.Frame(root, bg="#bdbdbd")
exportOBJbuttonFrame.place(relwidth=0.16, relheight=0.121, x=167, y=510)

exportMTLbuttonFrame = tk.Frame(root, bg="#bdbdbd")
exportMTLbuttonFrame.place(relwidth=0.16, relheight=0.121, x=303, y=510)

#Open Buttons
openOBJSequencefile = tk.Button(buttonOBJSequenceFrame, text="Open OBJ Sequence Folder", padx=100, pady=10, fg="black", bg = "white" , command=addObjSequence).pack()
openOBJfile = tk.Button(buttonOBJFrame, text="Open OBJ File", padx=100, pady=10, fg="black", bg = "white" , command=addObj).pack()
openMTLfile = tk.Button(buttonMTLFrame, text="Open MTL File", padx=100, pady=10, fg="black", bg = "white" , command=addMtl).pack()

#Convert Buttons
convertFile = tk.Button(exportOBJSequencebuttonFrame, text="Convert OBJ Sequence", padx=150, pady=30, fg="black", bg = "white", command=convertObjSequence).pack()
convertFile = tk.Button(exportOBJbuttonFrame, text="Convert OBJ", padx=150, pady=30, fg="black", bg = "white", command=convertObj).pack()
convertFile = tk.Button(exportMTLbuttonFrame, text="Convert MTL", padx=150, pady=30, fg="black", bg = "white", command=convertMtl).pack()

#Add Version Text
canvas.create_text(30, 20, text=version, fill="white", font=('Arial 10'), anchor='w')
canvas.pack(fill='both')

#Default Values At Start
objsequence.append(OBJSequenceerrortext)
defaultOBJSequencetext = tk.Label(directoryOBJSequenceFrame, text=objsequence, bg="#ffffff")
defaultOBJSequencetext.pack(side=tk.LEFT, fill='both')
objs.append(OBJerrortext)
defaultOBJtext = tk.Label(directoryOBJFrame, text=objs, bg="#ffffff")
defaultOBJtext.pack(side=tk.LEFT, fill='both')
mtls.append(MTLerrortext)
defaultMTLtext = tk.Label(directoryMTLFrame, text=mtls, bg="#ffffff")
defaultMTLtext.pack(side=tk.LEFT, fill='both')

def widgetSpace():
    ttk.Label(framemtl, text='', justify='center').pack(fill='x')

#Create Checkbuttons
ttk.Label(framemtl, text='OBJ Export Settings', justify='center').pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Vertices", variable = CheckVerticies, onvalue = 1, offvalue = 0).pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Faces", variable = CheckFaces, onvalue = 1, offvalue = 0).pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Normals", variable = CheckNormals, onvalue = 1, offvalue = 0).pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Texture Coords", variable = CheckTextureCoords, onvalue = 1, offvalue = 0).pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Use Materials", variable = CheckMaterials, onvalue = 1, offvalue = 0).pack(fill='x')

#Console
container = ttk.Frame(frame)
scrollcanvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=scrollcanvas.yview)
scrollable_frame = ttk.Frame(scrollcanvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: scrollcanvas.configure(
        scrollregion=scrollcanvas.bbox("all")
    )
)

scrollcanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollcanvas.configure(yscrollcommand=scrollbar.set)

container.pack()
scrollcanvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
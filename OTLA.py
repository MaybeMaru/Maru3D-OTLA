from distutils.log import error
from tabnanny import check
import tkinter as tk
from tkinter import filedialog, Text, ttk, messagebox
import os

root = tk.Tk()
root.iconbitmap('icon.ico')
root.title('FNF Maru3D : Obj to Lua Array Converter')
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
    ttk.Label(scrollable_frame, text=txt, anchor='w').pack(fill='both')

def clearWidgets():
    for widget in directoryOBJFrame.winfo_children():
        widget.destroy()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def clearWidgets2():
    for widget in directoryMTLFrame.winfo_children():
        widget.destroy()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def clearWidgets3():
    for widget in directoryOBJSequenceFrame.winfo_children():
        widget.destroy()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def addObjSequence():

    clearWidgets3()

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
    
    clearWidgets()

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

    clearWidgets2()

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

def convertObjSequence():

    for sequence in objsequence:
        for path in os.listdir(sequence):
            if os.path.isfile(os.path.join(sequence, path)):
                name, extension = os.path.splitext(path)
                if extension == ".obj":

                    #sequence -> path without the file
                    #path -> file name with extension
                        #name -> name duh
                        #extension -> extension dumbass
                    folderobjframe = os.path.join(sequence, path) #this is var has the path of every frame to convert
                    print(folderobjframe)

                    with open(folderobjframe) as f:
                        lines = f.readlines()

                    dir = "export/"+"frames/"
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

                        if CheckVerticies.get() == 1:
                            exporttext.write("vertices = {\n")
                            for line in lines:
                                if line.startswith("v "):
                                    finalline = line.lstrip("v ")
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == (" "):
                                            exporttext.write(",")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},")
                            exporttext.write("};\n")
                
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
                                    exporttext.write("\n{")
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
                            
                                    exporttext.write("},")
                            exporttext.write("};\n")

                        if CheckNormals.get() == 1:
                            exporttext.write("normals = {\n")
                            for line in lines:
                                if line.startswith("vn "):
                                    finalline = line.lstrip("vn ")
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == (" "):
                                            exporttext.write(",")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},")
                            exporttext.write("};\n")

                        if CheckTextureCoords.get() == 1:
                            exporttext.write("texturecoords = {\n")
                            for line in lines:
                                if line.startswith("vt "):
                                    finalline = line.lstrip("vt ")
                                    exporttext.write("{")
                                    for char in finalline:
                                        if char == (" "):
                                           exporttext.write(",")
                                        else:
                                            exporttext.write(char)
                                    exporttext.write("},")
                            exporttext.write("};\n")

                        exporttext.write("\nreturn {vertices, faces, normals, texturecoords, usematerials};")

                        #print("Finished OBJ Sequence "+name+" Export")
                        #ttk.Label(scrollable_frame, text="OBJ export finished as "+name+".lua", anchor='w').pack(fill='both')
                    #instert converter shit
                makeConsoleText("OBJ export finished as "+name+".lua")

def convertObj():

    for obj in objs:

        if objs[0] == OBJerrortext:
            errorReason = OBJerrortext
            messagebox.showerror('Error', 'Error: ' + errorReason)
        else:
            with open(obj) as f:
                lines = f.readlines()

            file_dir_name = os.path.basename(obj)
            file_dir_name = os.path.splitext(file_dir_name)[0]

            dir = "export/"+file_dir_name
            if not os.path.exists(dir):
                os.mkdir(dir)

            with open(dir+'/model.lua', 'w') as exporttext:
                exporttext.write("--Converted using "+version+"\n\n")

                if CheckMaterials.get() == 1:
                    exporttext.write("local usematerials = true\n")
                else:
                    exporttext.write("local usematerials = false\n")

                exporttext.write("local vertices = {}\n")
                exporttext.write("local faces = {}\n")
                exporttext.write("local normals = {}\n")
                exporttext.write("local texturecoords = {}\n\n")

                if CheckVerticies.get() == 1:
                    exporttext.write("vertices = {\n")
                    for line in lines:
                        if line.startswith("v "):
                            finalline = line.lstrip("v ")
                            exporttext.write("{")
                            for char in finalline:
                                if char == (" "):
                                    exporttext.write(",")
                                else:
                                    exporttext.write(char)
                            exporttext.write("},")
                    exporttext.write("};\n")
                
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
                            exporttext.write("\n{")
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
                            
                            exporttext.write("},")
                    exporttext.write("};\n")

                if CheckNormals.get() == 1:
                    exporttext.write("normals = {\n")
                    for line in lines:
                        if line.startswith("vn "):
                            finalline = line.lstrip("vn ")
                            exporttext.write("{")
                            for char in finalline:
                                if char == (" "):
                                    exporttext.write(",")
                                else:
                                    exporttext.write(char)
                            exporttext.write("},")
                    exporttext.write("};\n")

                if CheckTextureCoords.get() == 1:
                    exporttext.write("texturecoords = {\n")
                    for line in lines:
                        if line.startswith("vt "):
                            finalline = line.lstrip("vt ")
                            exporttext.write("{")
                            for char in finalline:
                                if char == (" "):
                                   exporttext.write(",")
                                else:
                                    exporttext.write(char)
                            exporttext.write("},")
                    exporttext.write("};\n")

                exporttext.write("\nreturn {vertices, faces, normals, texturecoords, usematerials};")

                print("Finished OBJ Export")
                ttk.Label(scrollable_frame, text="OBJ export finished as "+"model.lua", anchor='w').pack(fill='both')

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
                print("Finished MTL Export")
                ttk.Label(scrollable_frame, text="MTL export finished as "+"materials.lua", anchor='w').pack(fill='both')

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

exportOBJSequencebuttonFrame = tk.Frame(root, bg="#bdbdbd")
exportOBJSequencebuttonFrame.place(relwidth=0.16, relheight=0.121, x=30, y=510)

exportOBJbuttonFrame = tk.Frame(root, bg="#bdbdbd")
exportOBJbuttonFrame.place(relwidth=0.16, relheight=0.121, x=167, y=510)

exportMTLbuttonFrame = tk.Frame(root, bg="#bdbdbd")
exportMTLbuttonFrame.place(relwidth=0.16, relheight=0.121, x=303, y=510)

openOBJSequencefile = tk.Button(buttonOBJSequenceFrame, text="Open OBJ Sequence Folder", padx=100, pady=10, fg="black", bg = "white" , command=addObjSequence)
openOBJSequencefile.pack()

openOBJfile = tk.Button(buttonOBJFrame, text="Open OBJ File", padx=100, pady=10, fg="black", bg = "white" , command=addObj)
openOBJfile.pack()

openMTLfile = tk.Button(buttonMTLFrame, text="Open MTL File", padx=100, pady=10, fg="black", bg = "white" , command=addMtl)
openMTLfile.pack()

convertFile = tk.Button(exportOBJSequencebuttonFrame, text="Convert OBJ Sequence", padx=150, pady=30, fg="black", bg = "white", command=convertObjSequence)
convertFile.pack()

convertFile = tk.Button(exportOBJbuttonFrame, text="Convert OBJ", padx=150, pady=30, fg="black", bg = "white", command=convertObj)
convertFile.pack()

convertFile = tk.Button(exportMTLbuttonFrame, text="Convert MTL", padx=150, pady=30, fg="black", bg = "white", command=convertMtl)
convertFile.pack()

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

C1 = ttk.Checkbutton(framemtl, text = "Vertices", variable = CheckVerticies, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Faces", variable = CheckFaces, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Normals", variable = CheckNormals, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Texture Coords", variable = CheckTextureCoords, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Use Materials", variable = CheckMaterials, onvalue = 1, offvalue = 0)
C1.pack(fill='x')

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
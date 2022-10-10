import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os

root = tk.Tk()
#root.iconbitmap('icon.ico')
root.title('Maru3D : OBJ To LUA Array Converter')
root.resizable(False, False)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

version = 'Maru3D OTLA ' + 'v0.5.1'
errorMessages = ['No OBJ Sequence Folder Loaded', 'No OBJ File Loaded', 'No MTL File Loaded']

#Setup shit
objsequence, objs, mtls = [],[],[]

s = ttk.Style()
s.configure('.', font=('Arial', 11))

#CheckBoxes variables
CheckVerticies, CheckFaces, CheckNormals, CheckTextureCoords, CheckMaterials = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()

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
    if filename == "":
        objsequence.append(errorMessages[0])
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
        objs.append(errorMessages[1])
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
        mtls.append(errorMessages[2])
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
                                    finalline = line.removeprefix("v ")
                                    finalline = finalline.removeprefix(" ")
                                    finalline = finalline.rstrip()
                                    finalline = finalline.replace(" ", ",")  
                                    exporttext.write("{"+finalline)
                                    exporttext.write("},\n")
                            exporttext.write("};\n")
                
                        #Get Faces Code
                        if CheckFaces.get() == 1 :
                            exporttext.write("faces = {\n")
                            for line in lines:

                                if CheckMaterials.get() == 1:
                                    if line.startswith("usemtl "):
                                        material = line.removeprefix("usemtl ")
                                        material = material.rstrip()
                                        material = material.replace(" ", "")
        
                                if line.startswith("f "):
                                    vert_count = 1

                                    finalline = line.removeprefix("f ")
                                    finalline = finalline.rstrip()
                                    finalline = finalline.replace('//','/')
                                    finalline = finalline.replace("/", ",")

                                    for letter in finalline:
                                        if letter == " ":
                                            vert_count = 1 + vert_count
                                    if vert_count > 3:
                                        exporttext.write('--More than 3 vertex ('+vert_count+'), might not work correctly ')   

                                    finalline = finalline.replace(" ", "}, {")  
                                    exporttext.write("{ vertex = {{"+finalline+"}},")
        
                                    if CheckMaterials.get() == 1:
                                        exporttext.write(' mat = "'+material+'",')

                                    exporttext.write("},\n")
                            exporttext.write("};\n")

                        #Get Normals Code
                        if CheckNormals.get() == 1:
                            exporttext.write("normals = {\n")
                            for line in lines:
                                if line.startswith("vn "):
                                    finalline = line.removeprefix("vn ")
                                    finalline = finalline.rstrip()
                                    finalline = finalline.replace(" ", ",")  
                                    exporttext.write("{"+finalline)
                                    exporttext.write("},\n")
                            exporttext.write("};\n")

                        #Get Texture Coords Code
                        if CheckTextureCoords.get() == 1:
                            exporttext.write("texturecoords = {\n")
                            for line in lines:
                                if line.startswith("vt "):
                                    finalline = line.removeprefix("vt ")
                                    finalline = finalline.rstrip()
                                    finalline = finalline.replace(" ", ",")  
                                    exporttext.write("{"+finalline)
                                    exporttext.write("},\n")
                            exporttext.write("};\n")

                        exporttext.write("\nreturn {vertices = vertices, faces = faces, normals = normals, textcoords = texturecoords, usemats = usematerials};")

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
                    convertOBJcode(daPath, daObject, 'frames/', errorMessages[0], True)
        else:
            messagebox.showerror('Error', 'Error: ' + errorMessages[0])

def convertObj():

    for obj in objs:
        objFolder = os.path.basename(obj)
        objFolder = os.path.splitext(objFolder)[0]
        objFile = os.path.splitext(obj)
        objFile = objFolder+objFile[1]
        name, extension = os.path.splitext(objFile)
        convertOBJcode(obj, objFile, name+'/', errorMessages[1], False)

def convertMtl():
    for mtl in mtls:
        if mtl == errorMessages[2]:
            errorReason = errorMessages[2]
            messagebox.showerror('Error', 'Error: ' + errorReason)
        else:
            name, extension = os.path.splitext(mtl)
            if os.path.isfile(mtl) and (extension == '.mtl' or extension == '.txt'):
                with open(mtl) as f:
                        lines = f.readlines()

                file_dir_name = os.path.basename(mtl)
                file_dir_name = os.path.splitext(file_dir_name)[0]

                dir = "export/"+file_dir_name
                if not os.path.exists(dir):
                    os.mkdir(dir)

                with open(dir+'/materials.lua', 'w') as exporttext:
                    exporttext.write("--Converted using "+version+"\n\n")

                    exporttext.write("local materials = {}")
                    exporttext.write("\nmaterials = {\n")
                    boob = 0; ass = 0
                    for line in lines:
                        line = line.replace("\t", "")

                        #New Material
                        if line.startswith("newmtl "):
                            #Start New Material Shit
                            if ass < boob:
                                exporttext.write('},\n')
                                ass = boob
                            boob = boob+1

                            finalline = line.removeprefix("newmtl ")
                            finalline = finalline.rstrip()
                            finalline = finalline.replace(" ", "")
                            daMaterial = finalline
                            exporttext.write('{ name = "'+daMaterial+'",')

                        #Solid Color
                        if line.startswith("Kd "):
                            finalline = line.removeprefix("Kd ")
                            finalline = finalline.rstrip()

                            finalline = finalline.replace(" ", ",")   
                            exporttext.write(' kd = {'+finalline+"},")

                        #Texture
                        if line.startswith("map_Kd "):
                            finalline = line.removeprefix("map_Kd ")
                            finalline = finalline.rstrip()
                            print(finalline)
                            finalline = '"'+finalline+'"'
                            
                            finalline = finalline.replace(" ", ",")    
                            exporttext.write(' map_kd = '+finalline+",")

                    exporttext.write("}\n};")
                    exporttext.write("\nreturn materials;")
                    makeConsoleText("MTL export finished as "+"materials.lua")
                    makeConsoleText("In "+ dir+'/materials.lua')
            else:
                messagebox.showerror('Error', 'Error: ' + 'Incorrect file type\nOnly MTL and TXT files are allowed')

#Create Frames, Buttons n shit

canvas = tk.Canvas(root, height = 600, width=800, bg="#828282")
canvas.pack()

directoryOBJSequenceFrame = tk.Frame(root, bg="#bdbdbd"); directoryOBJSequenceFrame.place(relwidth=0.5, relheight=0.07, x=30, y=40)
buttonOBJSequenceFrame = tk.Frame(root, bg="#bdbdbd"); buttonOBJSequenceFrame.place(relwidth=0.2, relheight=0.07, x=450, y=40)

directoryOBJFrame = tk.Frame(root, bg="#bdbdbd"); directoryOBJFrame.place(relwidth=0.5, relheight=0.07, x=30, y=100)
buttonOBJFrame = tk.Frame(root, bg="#bdbdbd"); buttonOBJFrame.place(relwidth=0.2, relheight=0.07, x=450, y=100)

directoryMTLFrame = tk.Frame(root, bg="#bdbdbd"); directoryMTLFrame.place(relwidth=0.5, relheight=0.07, x=30, y=160)
buttonMTLFrame = tk.Frame(root, bg="#bdbdbd"); buttonMTLFrame.place(relwidth=0.2, relheight=0.07, x=450, y=160)

frame = tk.Frame(root, bg="#bdbdbd"); frame.place(relwidth=0.5, relheight=0.4, x=30, y=235)
framemtl = tk.Frame(root, bg="#bdbdbd"); framemtl.place(relwidth=0.40, relheight=0.576, x=450, y=235)

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
objsequence.append(errorMessages[0])
defaultOBJSequencetext = tk.Label(directoryOBJSequenceFrame, text=objsequence, bg="#ffffff")
defaultOBJSequencetext.pack(side=tk.LEFT, fill='both')
objs.append(errorMessages[1])
defaultOBJtext = tk.Label(directoryOBJFrame, text=objs, bg="#ffffff")
defaultOBJtext.pack(side=tk.LEFT, fill='both')
mtls.append(errorMessages[2])
defaultMTLtext = tk.Label(directoryMTLFrame, text=mtls, bg="#ffffff")
defaultMTLtext.pack(side=tk.LEFT, fill='both')

#Create Checkbuttons
def widgetSpace():
    ttk.Label(framemtl, text='', justify='center').pack(fill='x')

ttk.Label(framemtl, text='OBJ Export Settings', justify='center').pack(fill='x');                                                   widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Vertices", variable = CheckVerticies, onvalue = 1, offvalue = 0).pack(fill='x');             widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Faces", variable = CheckFaces, onvalue = 1, offvalue = 0).pack(fill='x');                    widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Normals", variable = CheckNormals, onvalue = 1, offvalue = 0).pack(fill='x');                widgetSpace()
C1 = ttk.Checkbutton(framemtl, text = "Texture Coords", variable = CheckTextureCoords, onvalue = 1, offvalue = 0).pack(fill='x');   widgetSpace()
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
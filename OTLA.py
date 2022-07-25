from tabnanny import check
import tkinter as tk
from tkinter import filedialog, Text, ttk
import os

root = tk.Tk()
root.iconbitmap('icon.ico')
root.title('FNF Maru3D : Obj to Lua Array Converter')
root.resizable(False, False)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

files = []

CheckVerticies = tk.IntVar()
CheckFaces = tk.IntVar()
CheckNormals = tk.IntVar()
CheckTextureCoords = tk.IntVar()

version = 'Maru3D OTLA ' + 'v0.4'

def addObj():

    for widget in names.winfo_children():
        widget.destroy()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    files.clear()
    filename =filedialog.askopenfilename(initialdir="/", title="Select 3D Model", 
    filetypes=((".obj", "*.obj"), (".txt", "*.txt"),("all files", "*.*")))
    if filename == "":
        files.append('No File Loaded')
    else:
        files.append(filename)    

    print(files)

    for widget in names.winfo_children():
        widget.destroy()

    label = tk.Label(names, text=files, bg="#ffffff")
    label.pack()

def convertObj():

    for file in files:

        if not file == "":

            with open(file) as f:
                lines = f.readlines()

            with open('export/model.lua', 'w') as exporttext:
                exporttext.write("--Converted using "+version+"\n\n")

                exporttext.write("vertices = {}\n")
                exporttext.write("faces = {}\n")
                exporttext.write("normals = {}\n")
                exporttext.write("texturecoords = {}\n\n")

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
                        if line.startswith("f "):
                            finalline = line.lstrip("f ")
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

                exporttext.write("\nreturn {vertices, faces, normals, texturecoords};")

                print("export finished successfully")

                with open('export/model.lua') as previewtext:
                    lines = previewtext.readlines()
                    ttk.Label(scrollable_frame, text='Exported File Preview:\n').pack(fill='both')

                    for line in lines:
                        ttk.Label(scrollable_frame, text=line, anchor='w').pack(fill='both')

canvas = tk.Canvas(root, height = 600, width=800, bg="#371142")
canvas.pack()

canvas.create_text(10, 15, text=version, fill="white", font=('Arial 10'), anchor='w')
canvas.pack(fill='both')

frame = tk.Frame(root, bg="#725572")
frame.place(relwidth=0.5, relheight=0.8, relx=0.05, rely=0.1)

framemtl = tk.Frame(root, bg="#725572")
framemtl.place(relwidth=0.35, relheight=0.8, relx=0.6, rely=0.1)

names  = tk.Frame(frame, bg="#ffffff")
names.place(relwidth=0.8, relheight=0.2, relx=0.1, rely=0.1)

preview  = tk.Frame(frame, bg="#9692bb")
preview.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.15)

frame2 = tk.Frame(frame, bg="#2b0a4f")
frame2.place(relwidth=1, relheight=1.12, relx=0, rely=0.8)

openFile = tk.Button(frame2, text="Open 3D Model File", padx=100, pady=5, fg="white", bg = "black", command=addObj)
openFile.pack()

convertFile = tk.Button(frame2, text="Convert To Lua", padx=112, pady=5, fg="white", bg = "black", command=convertObj)
convertFile.pack()

label = tk.Label(names, text='{No File Loaded}', bg="#ffffff")
label.pack()



ttk.Label(framemtl, text='Export Selection:\n').pack(fill='x')

C1 = ttk.Checkbutton(framemtl, text = "Vertices", variable = CheckVerticies, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
C1 = ttk.Checkbutton(framemtl, text = "Faces", variable = CheckFaces, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
C1 = ttk.Checkbutton(framemtl, text = "Normals", variable = CheckNormals, onvalue = 1, offvalue = 0)
C1.pack(fill='x')
C1 = ttk.Checkbutton(framemtl, text = "Texture Coords", variable = CheckTextureCoords, onvalue = 1, offvalue = 0)
C1.pack(fill='x')

container = ttk.Frame(preview)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
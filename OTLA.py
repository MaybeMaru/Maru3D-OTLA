import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()

files = []

def addObj():

    for widget in names.winfo_children():
        widget.destroy()

    filename =filedialog.askopenfilename(initialdir="/", title="Select 3D Model", 
    filetypes=((".obj", "*.obj"), (".txt", "*.txt"),("all files", "*.*")))
    files.append(filename)
    print(filename)

    for file in files:
        label = tk.Label(names, text=file, bg="#ffffff")
        label.pack()

def convertObj():

    for file in files:

        if not file == "":

            with open(file) as f:
                lines = f.readlines()

            with open('model.lua', 'w') as exporttext:
                exporttext.write("--Coverted using Maru3D OTLA\n")

                exporttext.write("vertex = {\n")

                for line in lines:

                    if line.startswith("v "):
                        finalline = line.lstrip("v ")
                        exporttext.write("{ ")
                        for char in finalline:
                            
                            if char == (" "):
                                exporttext.write(",")
                            else:
                                exporttext.write(char)

                        exporttext.write("}, \n")

                exporttext.write("};\n")

                exporttext.write("faces = {\n")
                for line in lines:
                    
                    if line.startswith("f "):
                        finalline = line.lstrip("f ")
                        exporttext.write("{ ")

                        exporttext.write("{ ")
                        for char in finalline:

                            if char == ("/"):
                                exporttext.write(",")
                            elif char == (" "):
                                exporttext.write("}, {")
                            else:
                                exporttext.write(char)

                        exporttext.write("}, ")
                        exporttext.write("}, \n")

                exporttext.write("};\n")
                exporttext.write("return {vertex, faces};")
                print("export finished successfully")

                for x in range(0, 10):
                    label = tk.Label(preview, text='Export Finished Succesfully!!!!', bg="#ffffff")
                    label.pack()

canvas = tk.Canvas(root, height = 700, width=700, bg="#371142")
canvas.pack()

frame = tk.Frame(root, bg="#725572")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

names  = tk.Frame(frame, bg="#ffffff")
names.place(relwidth=0.8, relheight=0.2, relx=0.1, rely=0.1)

preview  = tk.Frame(frame, bg="#9692bb")
preview.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.15)

frame2 = tk.Frame(frame, bg="#2b0a4f")
frame2.place(relwidth=1, relheight=0.1, relx=0, rely=0.8)

openFile = tk.Button(frame2, text="Open 3D Model File", padx=10, pady=5, fg="white", bg = "black", command=addObj)
openFile.pack()

convertFile = tk.Button(frame2, text="Convert to .lua", padx=10, pady=5, fg="white", bg = "black", command=convertObj)
convertFile.pack()

root.iconbitmap('icon.ico')
root.title('FNF Maru3D : Obj to Lua Array Converter')

root.mainloop()
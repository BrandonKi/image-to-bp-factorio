# this is by far the worst thing I've ever written
# wow

from zlib import *
from base64 import *
from json import *
from PIL import ImageTk, Image
import numpy as np
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pyperclip

window = None
image = None
final = None
graphic = None
canvas = None
progressBar = None

def main():
    global window
    global canvas
    global image
    global final
    global graphic
    global progressBar

    window = tk.Tk()
    window.title("BP UI")
    # window.size(640, 480)

    frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
    btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)
    btn_convert = tk.Button(frm_buttons, text="Convert", command=convert)
    btn_copy = tk.Button(frm_buttons, text="Copy To Clipboard", command=copy)

    progressBar = Progressbar(window,orient=tk.HORIZONTAL,length=200,mode="determinate",takefocus=True,maximum=100)

    canvas = tk.Canvas(window, width = 300, height = 300)
    canvas.pack()

    # graphic = tk.Label()
    # graphic.place(x=0, y=0)

    btn_open.grid(row=0, column=0)
    btn_save.grid(row=0, column=1)
    btn_convert.grid(row=0, column=2)
    btn_copy.grid(row=0, column=3)
    frm_buttons.pack(side=tk.BOTTOM)
    progressBar.pack(side=tk.BOTTOM)   



    window.mainloop()

def convert():
    global window
    global canvas
    global image
    global final
    global graphic
    global progressBar


    pallette = np.array([[41, 40, 41], [49, 49, 41], [58, 61, 58], [82, 81, 74], [107, 109, 107], [181, 142, 33], [115, 93, 25]])
    picture = np.array(image)
    print(picture.shape)
    new_image = np.empty_like(picture)

    progressBar.config(maximum=picture.shape[0]/10)

    for i in range(0, picture.shape[0]):
        if i % 10 == 0:
            progressBar.step()            
            window.update()
        row = picture[i]
        for x in range(0, picture.shape[1]):
            p = row[x]
            closest = pallette[0]
            smallest_distance = ((pallette[0][0]-p[0])**2 + (pallette[0][1]-p[1])**2 + (pallette[0][2]-p[2])**2)
            for color in pallette:
                dist = ((color[0]-p[0])**2 + (color[1]-p[1])**2 + (color[2]-p[2])**2)
                if dist < smallest_distance:
                    closest = color
                    smallest_distance = dist
            new_image[i][x] = closest

    image = new_image
    final = Image.fromarray(image)
    img = ImageTk.PhotoImage(final)
    # final.show()
    canvas.config(width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img

def copy():
    global window
    global canvas
    global image
    global final
    global graphic
    global progressBar

    progressBar.config(maximum=image.shape[0]/10)

    convert = {(41, 40, 41): 'kr-black-reinforced-plate', (49, 49, 41): 'refined-concrete', (58, 61, 58): 'concrete', (82, 81, 74): 'stone-path', (107, 109, 107): 'kr-white-reinforced-plate', (181, 142, 33): 'hazard-concrete-left', (115, 93, 25): 'refined-hazard-concrete-left'}
    result = {"blueprint": {"icons": [{"signal": {"type": "item", "name": "stone-brick"}, "index": 1}], "tiles":[], "item":"blueprint", "version": 281479276658688}}
    for i in range(0, image.shape[0]):
        if i % 10 == 0:
            progressBar.step()            
            window.update()
        row = image[i]
        for x in range(0, image.shape[1]):
            p = row[x]
            result["blueprint"]["tiles"].append({"position":{"x":x, "y":i}, "name": convert[tuple(p)]})

    # print(dumps(result, indent=4))
    pyperclip.copy('0' + repr(b64encode(compress(bytes(dumps(result), 'utf-8'), 9)))[2:-1])

def open_file():
    global image
    global window

    filepath = askopenfilename(
        filetypes=[("All Files", "*.*")]
    )
    image = Image.open(filepath).convert('RGB')
    img = ImageTk.PhotoImage(image)  
    # image.show()
    # canvas.geometry(f"{image.width()}x{image.height()}")
    canvas.config(width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img

def save_file():
    filepath = asksaveasfilename(
        defaultextension=".png",
        filetypes=[("JPG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")],
    )
    final.save(filepath)

if __name__ == '__main__':
    main()
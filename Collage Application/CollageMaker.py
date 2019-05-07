
from tkinter import *
import argparse
import os
import random
from PIL import Image

def make_collage(images, filename, width, init_height):

    if not images:
        print('No images for collage found!')
        return False

    margin_size = 0
    
    while True:
    
        images_list = images[:]
        coefs_lines = []
        images_line = []
        x = 0
        while images_list:
        
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
        
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + margin_size
            images_line.append(img_path)
        
        coefs_lines.append((float(x) / width, images_line))

        
        if len(coefs_lines) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
        
            init_height -= 10
        else:
            break

    
    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    if not out_height:
        print('Height of collage could not be 0!')
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    
    y = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    collage_image.save(filename)
    return True
	
	




 
window = Tk()
 
window.title("Picture Collage Creator")
 
window.geometry('500x300')
 
lbl1 = Label(window, text="Enter Picture Location")
 
lbl1.grid(column=0, row=0)
 
txt1 = Entry(window,width=40)

txt1.grid(column=1, row=0)

#lbl2 = Label(window, text="Enter output file Name")
 
#lbl2.grid(column=0, row=1)
 
#txt2 = Entry(window,width=10)
  
#txt2.grid(column=1, row=1)

lbl3 = Label(window, text="Output Width")
 
lbl3.grid(column=0, row=2)
 
txt3 = Entry(window,width=10)
  
txt3.grid(column=1, row=2)

lbl4 = Label(window, text="Output Height")
 
lbl4.grid(column=0, row=4)
 
txt4 = Entry(window,width=10)
  
txt4.grid(column=1, row=4)

#selected = BooleanVar()
#selected.set(False)
 
#rad1 = Radiobutton(window,text='Shuffle Pictures', variable=selected)
#rad1.grid(column=0, row=4)

def clicked():
	
	folder = txt1.get()
	fname  = 'Collage.png'
	width  = int(txt3.get())
	height = int(txt4.get())
#	shuffle = selected.get()
#	lbl.configure(text= res)
	files = [os.path.join(folder, fn) for fn in os.listdir(folder)]
	images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
	if not images:
		print('No images for making collage! Please select other directory with images!')
		exit(1)
	random.shuffle(images)
	print('Making collage...')
	res = make_collage(images, fname, width, height)
	if not res:
		print('Failed to create collage!')
		exit(1)
	print('Collage is ready!')
	window.quit()
 
btn = Button(window, text="Create Collage", command=clicked)
 
btn.grid(column=1, row=5)
 
window.mainloop()
from Tkinter import *
from PIL import Image, ImageTk
from ttk import Button, Label, Style, Entry

class Base(Frame):
	def __init__(self, parent):
		Frame.__init__(self, width=300, height=200, bg="black")
		self.parent = parent
		self.initUI()
	
	def initUI(self):
		self.parent.title("Story Creator")
		self.columnconfigure(0, pad=0)
		self.columnconfigure(1, pad=0)
		self.rowconfigure(0, pad=0)
		self.grid(row=0, column=0)
		
		logo = ImageTk.PhotoImage(Image.open("prelaunch_logo.png"))
		logolabel = Label(self, image=logo)
		logolabel.image = logo
		logolabel.grid(row=0, column=0)

    
    

root = Tk()
display = Base(root)
root.mainloop()
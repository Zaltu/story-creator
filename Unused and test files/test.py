from Tkinter import Tk, W, E
from ttk import Frame, Button, Label, Style
from ttk import Entry


class Base(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Story Creator")
        
        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')
        
		
        self.columnconfigure(0, pad=3)
       
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)	
        
        self.pack()

def main():
  
    root = Tk()
    app = Base(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
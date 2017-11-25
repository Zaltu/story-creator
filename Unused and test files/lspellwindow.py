from Tkinter import *
from ttk import Button, Style, Entry
import json_reader

okpressed=False

class Selection():

	def __init__(self):
		self.levelText = 0
		self.chosenSpell = ""
		global okpressed
		okpressed = False
	
	def main(self):
		root = Tk()
		root.overrideredirect(0)
		#root.geometry("900x450+560+315")
		app = LSF(root)
		root.mainloop()

class LSF(Frame):
	def __init__(self, parent):
		Frame.__init__(self)
		self.parent = parent
		self.iSpell00 = StringVar(self)
		self.compareval = self.iSpell00.get()
		self.initUI()
	
	def initUI(self):
		self.grid(row=0, column=0)
		Style().configure("TButton", padding=(0,5,0,5))
		self.ok = Button(self, text="Ok", command=self.okF)
		self.cancel = Button(self, text="Cancel", command=self.cancelF)
		self.level = Text(self, height=1, width=3)
		spellList = json_reader.data_list("spells")
		self.iSpellO = OptionMenu(self, self.iSpell00, *spellList)
		self.iSpellO.config(width=13)
	
		self.iSpellO.grid(row=0, column=0)
		self.level.grid(row=0, column=1)
		self.ok.grid(row=1, column=0)
		self.cancel.grid(row=1, column=1)
	
	
	def okF(self):
		self.chosenSpell = self.iSpell00.get()
		try:
			self.levelText = (int) (self.level.get(1.0, END))
			if not (self.chosenSpell == self.compareval):
				print "Ok"
				global okpressed
				okpressed = True
				self.quit()
				return
		except:
			print "Not an integer, not saved"
			return
		print "You must choose a spell"
	
	def cancelF(self):
		global okpressed
		okpressed = False
		self.quit()
		print "Cancel"
	
def callThis():
	window = Selection()
	window.main()
	print "Stupid idea"
	print okpressed
	if(okpressed):
		print "Spell successfully read"
		return (window.chosenSpell, window.levelText)
	return None

#callThis()
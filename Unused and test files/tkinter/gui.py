import Tkinter
#from PyQt4.QtGui import QApplication
import os
import sys
from Tkinter import *
from PIL import Image, ImageTk
from ttk import Button, Style, Entry
from creatures import Character, Persona
import json_reader
import slgui
#from popup import popup

class MainFrame():
	
	def __init__(self):
		print "Application started"
		
	def main(self):
		root = Tk()
		img = Tkinter.Image("photo", file=json_reader.buildPath("icon.gif"))
		root.tk.call('wm','iconphoto',root._w,img)
		root.overrideredirect(0)
		root.resizable(width=FALSE, height=FALSE)
		app = Base(root)
		root.mainloop()

class Base(Frame):

	def __init__(self, parent):
		Frame.__init__(self, bg='black')
		self.parent = parent
		self.initUI()
		
	def initUI(self):
		self.parent.title("Story Creator")
		self.grid(row=0, column=0)
		
		Style().configure("TButton", padding=(0,5,0,5), background='black')
		
		#logo = ImageTk.PhotoImage(Image.open(json_reader.buildPath("creator_logo.png")))
		#logolabel = Label(self, image=logo, bg='black')
		#logolabel.image = logo
		#logolabel.grid(row=0, column=0)
		
		intframe = Frame(self)
		intframe.configure(bg='black')
		intframe.grid(row=0, column=1)
		
		createSL = Button(intframe, text="Create Social Link", command = self.actionS)
		createSL.grid(row=0, column=0)
		
		createPersona = Button(intframe, text="Create Persona", command=self.actionP)
		createPersona.grid(row=1, column=0)
		
		createChar = Button(intframe, text="Create Character", command=self.actionC)
		createChar.grid(row=2, column=0)
		
		quit = Button(intframe, text="Quit", command=self.quit)
		quit.grid(row=3, column=0)
		
		#logolabel.config(highlightthickness=0)
		
	def actionP(self):
		print "Changed frame to Persona creator"
		app = persona_creator(self.parent)
		self.destroy()
	
	def actionC(self):
		print "Changed frame to Character creator"
		app = char_creator(self.parent)
		self.destroy()
		
	def actionS(self):
		print "Changed frame to SL creator"
		app = SL_creator(self.parent)
		self.destroy()
		
	def quit(self):
		sys.exit(0)

class SL_creator(Frame):

	def __init__(self, parent):
		Frame.__init__(self)
		self.parent = parent
		self.variable = StringVar(self)
		self.v = StringVar(self)
		self.level = StringVar(self)
		self.angle = StringVar(self)
		self.initUI()
		
	def initUI(self):
		self.parent.title("Social Link Creator")
		self.grid(row=0, column=0)
		
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')

		list = json_reader.data_list("arcanas")
		self.variable.set("Select Arcana")
		w = OptionMenu(self, self.variable, *list, command=self.showText)
		w.grid(row=0, column=1)
		
		select = Button(self, text="Select", command=self.context)
		select.grid(row=1, column=1)
		
		back = Button(self, text="Back", command=self.back)
		back.grid(row=2, column=1)
		
		self.v.set("")
		self.text = Label(self, textvariable=self.v, wraplength=500)
		self.text.grid(row=0, column=0, rowspan=3)
		
	def context(self):
		if self.variable.get() == "Select Arcana":
			return
		levs = []
		for x in range(1,11):
			levs.append("Level " + str(x))
		self.level.set(levs[0])
		self.levelOM = OptionMenu(self, self.level, *levs)
		self.levelOM.grid(row=1, column=2, columnspan=2)
		
		self.angs = []
		try:
			tempLink = json_reader.readLink(self.variable.get())
			print tempLink
			print self.variable.get()
			for decon in tempLink["cutscenes"]:
				self.angs.append("Angle " + str(decon)[str(decon).index("_")+1:] )
		except:
			pass
		if not self.angs:
			self.angs.append("No angles")
		self.angle.set(self.angs[0])
		self.angleOM = OptionMenu(self, self.angle, *self.angs)
		self.angleOM.grid(row=2, column=2, columnspan=2)
		
		self.addAngB = Button(self, text="Add Angle", command=self.addAngle)
		self.addAngB.grid(row=3, column=2)
		
		self.newAng = Text(self, height=1, width=5)
		self.newAng.grid(row=3, column=3)
		
		self.go = Button(self, text="Go", command=self.begin)
		self.go.grid(row=4, column=2, columnspan=2)
		
	def addAngle(self):
		try:
			(int)(self.newAng.get(1.0, END))
			if self.angs[0] == "No angles":
				self.angleOM["menu"].delete(0, "end")
			self.angleOM["menu"].add_command(label="Angle "+self.newAng.get(1.0, END), command=Tkinter._setit(self.angle, ("Angle "+self.newAng.get(1.0, END)).replace("\n", "")))
			self.angle.set(("Angle "+self.newAng.get(1.0, END)).replace("\n", ""))
			self.newAng.delete(1.0, END)
		except:
			popup("The Angle must be an integer", "Critical")
			print "Angle must be an integer"
		
	def showText(self, somthing):
		self.v.set(json_reader.readArcDesc(self.variable.get()))
		self.destroyContext()
		
	def destroyContext(self):
		try:
			self.levelOM.destroy()
			self.angleOM.destroy()
			self.addAngB.destroy()
			self.newAng.destroy()
			self.go.destroy()
		except:
			pass
		
	def begin(self):
		if self.angle.get() == "No angles":
			popup("An Angle must be selected.\nCreate angles by entering a number in the text box below and clicking \"Add Angle\"", "Critical")
			return
		enter_level = self.level.get()[self.level.get().index(" ")+1:]
		print enter_level
		enter_angle = self.angle.get()[self.angle.get().index(" ")+1:]
		print enter_angle
		print "Entered SL creation mode for arcana " + self.variable.get()
		self.parent.withdraw()
		self.destroyContext()
		sl = slgui.SLFrame(self.parent, self.variable.get(), (int)(enter_level), (int)(enter_angle))
		
	def back(self):
		print "Returned to main screen"
		app = Base(self.parent)
		self.destroy()
		


class persona_creator(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self)
		self.parent = parent
		self.infoFrame = None
		self.createFrame = None
		self.listP = None
		self.listLS = None
		self.listEL1 = None
		self.listEL2 = None
		
		self.nameT = None
		self.arcVar = StringVar(self)
		self.levelT = None
		self.textT = None
		self.strT = None
		self.magT = None
		self.endT = None
		self.agiT = None
		self.luckT = None
		self.her1 = StringVar(self)
		self.her2 = StringVar(self)
		self.slashVar = StringVar(self)
		self.strikeVar = StringVar(self)
		self.pierceVar = StringVar(self)
		self.fireVar = StringVar(self)
		self.iceVar = StringVar(self)
		self.elecVar = StringVar(self)
		self.windVar = StringVar(self)
		self.lightVar = StringVar(self)
		self.darkVar = StringVar(self)
		self.lsSpell = StringVar(self)
		self.compareval = self.lsSpell.get()
		self.iSpell00 = StringVar(self)
		self.iSpell01 = StringVar(self)
		self.iSpell10 = StringVar(self)
		self.iSpell11 = StringVar(self)
		self.iSpell20 = StringVar(self)
		self.iSpell21 = StringVar(self)
		self.iSpell30 = StringVar(self)
		self.iSpell31 = StringVar(self)
		
		self.initUI(True)
	
	def initUI(self, infoDump):
		self.parent.title("Persona Creator")
		self.grid(row=0, column=0)
		
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		
		if (infoDump):
			self.infoFrameDraw()
		else:
			self.createFrameDraw()
			
		self.initButtonFrame(infoDump)
		
		self.listP = Listbox(self)
		self.listP.grid(row=0, column=3, columnspan=2, rowspan=3)
		temp = json_reader.readPerNames()
		for name in temp:
			self.listP.insert(END, name)
		
	def initButtonFrame(self, infoDump):
		self.buttonFrame = Frame(self)
		self.buttonFrame.grid(row=3, column=0, columnspan=4)
		
		new = Button(self.buttonFrame, text="New", command=self.new)
		new.grid(row=4, column=0)
		
		back = Button(self.buttonFrame, text="Back", command=self.back)
		back.grid(row=4, column=4)
			
		remove = Button(self.buttonFrame, text="Remove", command=self.remove)
		remove.grid(row=4, column=3)
		
		edit = Button(self.buttonFrame, text="Edit", command=self.edit)
		edit.grid(row=4, column=2)
		
		if not (infoDump):
			save = Button(self.buttonFrame, text="Save", command=self.save)
			save.grid(row=4, column=1)
		
		
	def createFrameDraw(self):
		self.createFrame = Frame(self)
		self.createFrame.grid(row=0, column=0, rowspan=2, columnspan=2)
		
		self.iSpell00.set("")
		self.iSpell01.set("")
		self.iSpell10.set("")
		self.iSpell11.set("")
		self.iSpell20.set("")
		self.iSpell21.set("")
		self.iSpell30.set("")
		self.iSpell31.set("")
		
		self.lsdic = {}
		
		self.slashVar.set("Normal")
		self.strikeVar.set("Normal")
		self.pierceVar.set("Normal")
		self.fireVar.set("Normal")
		self.iceVar.set("Normal")
		self.elecVar.set("Normal")
		self.windVar.set("Normal")
		self.lightVar.set("Normal")
		self.darkVar.set("Normal")
	
		nameL = Label(self.createFrame, text="Name:")
		nameL.grid(row=0, column=0)
		self.nameT = Text(self.createFrame, height=1, width=15)
		self.nameT.grid(row=0, column=1)

		strL = Label(self.createFrame, text="Str")
		strL.grid(row=0, column=2)
		self.strT = Text(self.createFrame, height=1, width=3)
		self.strT.grid(row=0, column=3)
		magL = Label(self.createFrame, text="Mag")
		magL.grid(row=1, column=2)
		self.magT = Text(self.createFrame, height=1, width=3)
		self.magT.grid(row=1, column=3)
		endL = Label(self.createFrame, text="End")
		endL.grid(row=2, column=2)
		self.endT = Text(self.createFrame, height=1, width=3)
		self.endT.grid(row=2, column=3)
		agiL = Label(self.createFrame, text="Agi")
		agiL.grid(row=3, column=2)
		self.agiT = Text(self.createFrame, height=1, width=3)
		self.agiT.grid(row=3, column=3)
		luckL = Label(self.createFrame, text="Luck")
		luckL.grid(row=4, column=2)
		self.luckT = Text(self.createFrame, height=1, width=3)
		self.luckT.grid(row=4, column=3)
		
		resList = json_reader.data_list("resistances")
		resL = Label(self.createFrame, text="Resistance:")
		resL.grid(row=0, column=5)
		slashL = Label(self.createFrame, text="Slash")
		slashL.grid(row=1, column=5)
		slashO = OptionMenu(self.createFrame, self.slashVar, *resList)
		slashO.grid(row=1, column=6, sticky="ew")
		strikeL = Label(self.createFrame, text="Strike")
		strikeL.grid(row=2, column=5)
		strikeO = OptionMenu(self.createFrame, self.strikeVar, *resList)
		strikeO.grid(row=2, column=6, sticky="ew")
		pierceL = Label(self.createFrame, text="Pierce")
		pierceL.grid(row=3, column=5)
		pierceO = OptionMenu(self.createFrame, self.pierceVar, *resList)
		pierceO.grid(row=3, column=6, sticky="ew")
		fireL = Label(self.createFrame, text="Fire")
		fireL.grid(row=4, column=5)
		fireO = OptionMenu(self.createFrame, self.fireVar, *resList)
		fireO.grid(row=4, column=6, sticky="ew")
		iceL = Label(self.createFrame, text="Ice")
		iceL.grid(row=5, column=5)
		iceO = OptionMenu(self.createFrame, self.iceVar, *resList)
		iceO.grid(row=5, column=6, sticky="ew")
		elecL = Label(self.createFrame, text="Elec")
		elecL.grid(row=6, column=5)
		elecO = OptionMenu(self.createFrame, self.elecVar, *resList)
		elecO.grid(row=6, column=6, sticky="ew")
		windL = Label(self.createFrame, text="Wind")
		windL.grid(row=7, column=5)
		windO= OptionMenu(self.createFrame, self.windVar, *resList)
		windO.grid(row=7, column=6, sticky="ew")
		lightL = Label(self.createFrame, text="Light")
		lightL.grid(row=8, column=5)
		lightO = OptionMenu(self.createFrame, self.lightVar, *resList)
		lightO.grid(row=8, column=6, sticky="ew")
		darkL = Label(self.createFrame, text="Dark")
		darkL.grid(row=9, column=5)
		darkO = OptionMenu(self.createFrame, self.darkVar, *resList)
		darkO.grid(row=9, column=6, sticky="ew")
		
		spellList = json_reader.data_list("spells")
		self.listLS = Listbox(self.createFrame, height=18)
		self.listLS.grid(row=3, column=7, columnspan=2, rowspan=8)
		
		newLS = Button(self.createFrame, text="+", command=self.addLS)
		newLS.grid(row=2, column=7)
		delLS = Button(self.createFrame, text="DEL", command=self.delLS)
		delLS.grid(row=2, column=8)
		
		LSL = Label(self.createFrame, text="Learned Spells:")
		LSL.grid(row=0, column=7, columnspan=2)
		
		arcanaL = Label(self.createFrame, text="Arcana:")
		arcanaL.grid(row=1, column=0)
		list = json_reader.data_list("arcanas")
		self.arcVar.set("Fool") # default value
		arcO = OptionMenu(self.createFrame, self.arcVar, *list)
		arcO.grid(row=1, column=1)
		
		levelL = Label(self.createFrame, text="Level:")
		levelL.grid(row=2, column=0)
		self.levelT = Text(self.createFrame, height=1, width=3)
		self.levelT.grid(row=2, column=1)
		
		heritageL = Label(self.createFrame, text="Inherits:")
		heritageL.grid(row=3, column=0, columnspan=2)
		
		elements = json_reader.data_list("elements")
		self.listEL1 = OptionMenu(self.createFrame, self.her1, *elements)
		self.listEL1.config(width=5)
		self.listEL1.grid(row=4, column=0)
		self.listEL2 = OptionMenu(self.createFrame, self.her2, *elements)
		self.listEL2.config(width=5)
		self.listEL2.grid(row=4, column=1)
		
		iSpellL = Label(self.createFrame, text="Initial Spells:")
		iSpellL.grid(row=5, column = 0, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell00, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=6, column=0, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell01, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=6, column=2, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell10, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=7, column=0, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell11, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=7, column=2, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell20, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=8, column=0, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell21, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=8, column=2, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell30, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=9, column=0, columnspan=2)
		iSpellO = OptionMenu(self.createFrame, self.iSpell31, *spellList)
		iSpellO.config(width=13)
		iSpellO.grid(row=9, column=2, columnspan=2)
		
		textL = Label(self.createFrame, text="Info:")
		textL.grid(row=10, column=0)
		self.textT = Text(self.createFrame, height=5, width=40, wrap=WORD)
		self.textT.grid(row=10, column=1, columnspan=5)
		
		self.lslevel = Text(self.createFrame, height=1, width=3)
		self.lsSpellO = OptionMenu(self.createFrame, self.lsSpell, *spellList)
		self.lsSpellO.config(width=13)
	
		self.lsSpellO.grid(row=1, column=7)
		self.lslevel.grid(row=1, column=8)

	def addLS(self):
		print "Adding learned spell"
		self.chosenSpell = self.lsSpell.get()
		try:
			self.lstext = (int) (self.lslevel.get(1.0, END))
			if self.lstext <= (int)(self.levelT.get(1.0, END)):
				raise Exception("")
			if not (self.chosenSpell == self.compareval):
				print "Ok"
				self.lsdic[self.chosenSpell] = self.lslevel.get(1.0, END).replace("\n", "")
				self.listLS.insert(END, self.chosenSpell + " at level " + self.lslevel.get(1.0, END))
				return
		except:
			popup("You must enter a level that is greater than the Persona's level.", "Critical")
			print "Not an integer or level smaller than Persona's level, not saved"
			return
		popup("You must choose a spell", "Critical")
		print "You must choose a spell"
		
		
	def delLS(self):
		print "Deleting learned spell"
		key = ""
		i=0
		while (len(self.listLS.get(ANCHOR)) > i):
			if self.listLS.get(ANCHOR)[i] == " " and self.listLS.get(ANCHOR)[i+1] == "a" and self.listLS.get(ANCHOR)[i+2] == "t":
				break
			key+= self.listLS.get(ANCHOR)[i]
			i=i+1
		print key
		print self.lsdic.pop(key)
		self.listLS.delete(ANCHOR)
		
		
	def loadPer(self, name):
		data = json_reader.readP(name)
		self.nameT.delete(1.0, END)
		self.nameT.insert(1.0, data["name"])
		self.textT.delete(1.0, END)
		self.textT.insert(1.0, data["desc"])
		self.strT.delete(1.0, END)
		self.magT.delete(1.0, END)
		self.endT.delete(1.0, END)
		self.agiT.delete(1.0, END)
		self.luckT.delete(1.0, END)
		self.strT.insert(1.0, data["stats"][0])
		self.magT.insert(1.0, data["stats"][1])
		self.endT.insert(1.0, data["stats"][2])
		self.agiT.insert(1.0, data["stats"][3])
		self.luckT.insert(1.0, data["stats"][4])
		self.levelT.delete(1.0, END)
		self.levelT.insert(1.0, data["level"])
		self.her1.set(data["heritage"][0])
		self.her2.set(data["heritage"][1])
		self.slashVar.set(data["resistance"][0])
		self.strikeVar.set(data["resistance"][1])
		self.pierceVar.set(data["resistance"][2])
		self.fireVar.set(data["resistance"][3])
		self.iceVar.set(data["resistance"][4])
		self.elecVar.set(data["resistance"][5])
		self.windVar.set(data["resistance"][6])
		self.lightVar.set(data["resistance"][7])
		self.darkVar.set(data["resistance"][8])
		self.iSpell00.set(data["spellDeck"][0])
		self.iSpell01.set(data["spellDeck"][1])
		self.iSpell10.set(data["spellDeck"][2])
		self.iSpell11.set(data["spellDeck"][3])
		self.iSpell20.set(data["spellDeck"][4])
		self.iSpell21.set(data["spellDeck"][5])
		self.iSpell30.set(data["spellDeck"][6])
		self.iSpell31.set(data["spellDeck"][7])
		self.lsdic = data["spellLearn"]
		self.listLS.delete(0, END)
		for spell, level in self.lsdic.iteritems():
			self.listLS.insert(END, spell + " at level " + level)
		
		print "Loaded " + data["name"]
	
	def infoFrameDraw(self):
		self.infoFrame = Frame(self)
		self.infoFrame.grid(row=0, column=0, rowspan=2, columnspan=2)
		
		infoP = Label(self.infoFrame, text="")
		infoP.grid(row=0, column=0, rowspan=2, columnspan=2)
	
	def edit(self):
		try:
			if (self.listP.get(ANCHOR) != ""):
				if self.createFrame and not popup("Override any unsaved changes?", "Warning"):
					return
				self.loadPer(self.listP.get(ANCHOR))
		except:#To initialize createFrame UI before load
			if(self.listP.get(ANCHOR) != ""):
				temp = self.listP.get(ANCHOR)
				self.infoFrame.destroy()
				self.initUI(False)
				self.loadPer(temp)
			else:
				return
		print "Changed to edit frame"
	
	def save(self):
		print json_reader.buildPath('data/'+self.nameT.get(1.0, END).replace("\n", "")+".json")
		print os.path.exists(json_reader.buildPath('data/'+self.nameT.get(1.0, END).replace("\n", "")+".json"))
		if os.path.exists(json_reader.buildPath('data/'+self.nameT.get(1.0, END).replace("\n", "")+".json")):
			if not popup("Override existing Persona "+self.nameT.get(1.0, END).replace("\n", "")+"?", "Question"):
				return
		print "Saving"
		spellDeck = [self.iSpell00.get(), self.iSpell01.get(), self.iSpell10.get(), self.iSpell11.get(), self.iSpell20.get(), self.iSpell21.get(), self.iSpell30.get(), self.iSpell31.get()]
		stats = [self.strT.get(1.0, END).replace("\n", ""), self.magT.get(1.0, END).replace("\n", ""), self.endT.get(1.0, END).replace("\n", ""), self.agiT.get(1.0, END).replace("\n", ""), self.luckT.get(1.0, END).replace("\n", "")]
		res = [self.slashVar.get(), self.strikeVar.get(), self.pierceVar.get(), self.fireVar.get(), self.iceVar.get(), self.elecVar.get(), self.windVar.get(), self.lightVar.get(), self.darkVar.get()]
		try:
			(int)(self.levelT.get(1.0, END))
			(int)(self.strT.get(1.0, END))
			(int)(self.magT.get(1.0, END))
			(int)(self.endT.get(1.0, END))
			(int)(self.agiT.get(1.0, END))
			(int)(self.luckT.get(1.0, END))
		except:
			popup("There is a number entry that isn't valid.\nEntries requiring numbers are:\nLEVEL\nSTR\nMAG\nEND\nAGI\nLUCK", "Critical")
			print "Not Saved"
			return
		if not (self.nameT.get(1.0, END) and not self.nameT.get(1.0, END).isspace()):
			popup("No name entered for your Persona. Name is a required field.", "Critical")
			print "No Name, not saved"
			return
		toWrite = Persona(self.nameT.get(1.0, END).replace("\n", ""), self.arcVar.get(), self.levelT.get(1.0, END).replace("\n", ""), self.textT.get(1.0, END).replace("\n", ""), spellDeck, self.lsdic, stats, res, [self.her1.get(), self.her2.get()])
		json_reader.writeOneP(toWrite)
		temp = self.nameT.get(1.0, END).replace("\n", "")
		if (temp not in self.listP.get(0, END)):
			self.listP.insert(END, temp)
		self.loadPer(temp)
		print "Saved Persona"
	
	def remove(self):
		if self.listP.get(ANCHOR)=="":
			return
		if not popup("Are you certain you want to completely remove this Persona?\n(Cannot be undone)", "Warning"):
			return
		print "Removing Persona " + self.listP.get(ANCHOR)
		json_reader.deletePer(self.listP.get(ANCHOR))
		self.listP.delete(ANCHOR)
		
	
	def new(self):
		self.infoFrame.destroy()
		self.buttonFrame.destroy()
		self.initUI(False)
		print "Created"
	"""LEGACY
	def cancel(self):
		if not popup("Cancelling will lose any unsaved changes. Continue?", "Warning"):
			return
		print "Cancelled editing"
		self.createFrame.destroy()
		self.buttonFrame.destroy()
		self.initUI(True)
	"""	
	def back(self):
		print "Returned to main screen"
		app = Base(self.parent)
		self.destroy()
	
	
class char_creator(Frame):

	def __init__(self, parent):
		Frame.__init__(self)
		self.parent = parent
		self.var = IntVar()
		self.variable = StringVar(self)
		self.nameT = None
		self.infoT = None
		self.importantB = None
		self.initUI()
	
	def initUI(self):
		self.parent.title("Persona Creator")
		self.grid(row=0, column=0)
		
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		
		nameL = Label(self, text="Name:")
		nameL.grid(row=1, column=1)
		
		self.nameT = Text(self, height=1, width=25)
		self.nameT.grid(row=1, column=2)
		
		self.importantB = Checkbutton(self, text="Important?", variable=self.var)
		self.importantB.grid(row=1, column=3)
		
		infoL = Label(self, text="Info:")
		infoL.grid(row=2, column=1)
		
		self.infoT = Text(self, height=7, width=50, wrap=WORD)
		self.infoT.grid(row=2, column=2, columnspan=2)
		
		save = Button(self, text="Save", command=self.save)
		save.grid(row=4, column=1)
		
		edit = Button(self, text="Remove", command=self.remove)
		edit.grid(row=4, column=2)
		
		back = Button(self, text="Back", command=self.back)
		back.grid(row=4, column=3)
		
		names = json_reader.readCharNames()
		names.append("New")
		self.variable.set("New") # default value
		if len(names) == 1:
			w = OptionMenu(self, self.variable, "New", command=self.loadChar)
		else:
			w = OptionMenu(self, self.variable, *names, command=self.loadChar)
		w.grid(row=4, column=4)
	
	def loadChar(self, name):
		print "Loading..."
		self.importantB.deselect()
		self.nameT.delete(1.0, END)
		self.infoT.delete(1.0, END)
		if name == "New":
			return
		charTL = json_reader.readOne(name)
		if(charTL.getImportant()):
			self.importantB.select()
		self.nameT.insert(1.0, charTL.getName())
		self.infoT.insert(1.0, charTL.getDesc())
		print "Loaded character " + self.variable.get()
	
	def remove(self):
		if not popup("Are you certain you want to completely remove this character?\n(Cannot be undone)", "Warning"):
			return
		print "Removing character " + self.variable.get()
		json_reader.deleteChar(self.variable.get())
		self.initUI()
		self.importantB.deselect()
		print "Changed to edit frame"
	
	def save(self):
		if self.nameT.get(1.0, END).replace("\n", "") in ["New", ""]:
			popup("Sorry, your character cannot be called \""+self.nameT.get(1.0, END).replace("\n", "")+"\". That is a reserved keyword (and it's also a dumb name)", "Critical")
			return
		print "Saving"
		toWrite = Character(self.nameT.get(1.0, END).replace("\n", ""), self.infoT.get(1.0, END).replace("\n", ""), self.var.get())
		json_reader.writeOne(toWrite)
		temp = self.nameT.get(1.0, END).replace("\n", "")
		self.initUI()
		self.loadChar(temp)
		self.variable.set(temp)
		print "Saved"
		
	def back(self):
		print "Returned to main screen"
		app = Base(self.parent)
		self.destroy()
	
# Create an PyQT4 application object.
#a = QApplication(sys.argv)
mainframe = MainFrame()
mainframe.main()
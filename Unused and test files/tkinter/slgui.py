import Tkinter
from Tkinter import *
from PIL import Image, ImageTk
from ttk import Button, Style, Entry
from creatures import Character, Persona
from action import *
from sls import *
import json_reader
#from popup import popup
#from simulate import Simulation


class SLFrame(Toplevel):
		
	def __init__(self, pRootWindow, arcana, level, angle):
		self.rootWindow = pRootWindow
		print "Application started"
		Toplevel.__init__(self)
		img = Tkinter.Image("photo", file=json_reader.buildPath("icon.gif"))
		self.tk.call('wm','iconphoto',self._w,img)
		self.arcana = arcana
		self.level = level
		self.angle = angle
		self.linkstored = SocialLink(arcana)
		self.link = self.linkstored.startLink(level, angle)
		self.i = 0
		self.initUI()
		
	def initUI(self):
		self.title("Social Link Creator")
		
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')

		#simulate = Button(self, text="Simulate", command=self.simulate)
		#simulate.grid(row=2, column=3)

		back = Button(self, text="Back to Arcana selection", command=self.back)
		back.grid(row=2, column=2)
		
		SLBase(self)
		
	def back(self):
		self.destroy()
		self.rootWindow.deiconify()
	"""
	def simulate(self):
		self.withdraw()
		Simulation(self.link, self.arcana, self.level, self.angle)
		self.deiconify()
		print "Simulation Over"
	"""
	
	def writeSave():
		self.linkstored.setLink(self.link, self.level, self.angle)
		self.linkstored.save()
		
class SLBase(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, master=parent)
		self.parent = parent
		self.empty = True
		self.index = StringVar(self)
		self.load = 0
		self.initUI()
		self.grid(row=2, column=0, rowspan=2)
		
	def initUI(self):
		self.actions = self.parent.link.getIDs()#load here (load the hash list from sls.py) NOT LOADING FROM SLS BUT MATHGRAPH
		self.index.set("")
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		if len(self.actions)>0:
			self.empty = False
		else:
			self.actions.append("")
		
		if self.empty:
			start = Button(self, text="Start New", command=self.changeFrame)
			start.grid(row=1, column=1)
			
		actOM = OptionMenu(self, self.index, *self.actions, command=self.enter)
		actOM.config(width=5)
		actOM.grid(row=1, column=0, sticky="ew")
			
	def changeFrame(self):
		self.destroy()
		self.actions.index(self.index.get())
		self.parent.i = self.actions.index(self.index.get())
		print "Current index: " + str(self.parent.i)
		CreationContainer(self.parent, self)
		
	def enter(self, something):
		if self.index.get() is "":
			print "No valid action selected"
			return
		self.parent.i = self.actions.index(self.index.get())
		self.load = self.parent.link.getItem(self.actions.index(self.index.get()))
		enter = Button(self, text="Edit", command=self.changeFrame)
		enter.grid(row=0, column=1)
		
		
		
class CreationContainer(Frame):
	
	def __init__(self, parent, concF):
		Frame.__init__(self, master=parent)
		self.parent = parent
		self.type = StringVar(self)
		self.connection = StringVar(self)
		self.concF = concF
		self.load = concF.load
		self.initUI()
		self.grid(row=0, column=2, rowspan=2, columnspan=10)
		
	def initUI(self):
		self.actions = self.parent.link.getIDs()
		self.actions.append("New element")
		types = ["Info", "Speak", "Camera Change", "Movement"]
		self.type.set("Info")
		self.connection.set("New element")
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		
		self.save = Button(self, text="Save")
		self.save.grid(row=2, column=0)
		
		self.existing_connections = Listbox(self)
		self.populateExistingConnections()
		self.existing_connections.grid(row=1, rowspan=2, column=5)
		
		self.next = OptionMenu(self, self.connection, *self.actions)
		self.next.grid(row=3, column=2)
		
		self.window = None
		if self.load!=0:
			self.connection.set(self.concF.index.get())
		self.connect(True)
		self.connection.set("New element")
		
		actOM = OptionMenu(self, self.type, *types, command=self.changeFrame)
		actOM.config(width=25)
		actOM.grid(row=0, column=0, columnspan=2, sticky="ew")
		
		self.backB = Button(self, text="Back", command=self.back)
		self.backB.grid(row=3, column=4)
		
		self.lead = Label(self, text="Leads to:")
		self.lead.grid(row=3, column=1)
		
		self.connectB = Button(self, text="Connect", command=self.lightConnect)
		self.connectB.grid(row=3, column=3)
		
		self.delete = Button(self, text="Delete", command=self.removeElement)
		self.delete.grid(row=3, column=0)
		
		self.follow_path = Button(self, text="Enter linked element", command=self.follow)
		self.follow_path.grid(row=0, column=6, rowspan=2)
		
		self.rmvRel = Button(self, text="Remove this connection", command=self.removeRelation)
		self.rmvRel.grid(row=1, column=6, rowspan=2)
		
		self.conLab = Label(self, text="This action connects to:")
		self.conLab.grid(row=0, column=5)
		
	def removeRelation(self):
		if not popup("Are you sure you want to remove this relation?\n\nWARNING: ANY ACTIONS SOLELY DEPENDANT ON THIS RELATION WILL BE DELETED RECURSIVELY (TREE WILL BE PRUNED)"+
					"\n\ne.g.\nAction 1 => Action 2 => Action 3\nAction 1 =/> Action 2 => Action 3\nAction 1 => Nothing\n\nHowever:\nAction 1 => Action 2\nAction 5 => Action 2\n\n"+
					"Action 1 =/> Action 2\nAction 5 => Action 2\n\nAction 1 => Nothing\nAction 5 => Action 2", "Warning"):
			return
		self.parent.link.delRelation(self.parent.i, self.actions.index(self.existing_connections.get(ANCHOR)))
		self.populateExistingConnections()
		self.updateElementList()
		
	def removeElement(self):
		if not popup("Are you sure you want to remove this relation?\n\nWARNING: ANY ACTIONS SOLELY DEPENDANT ON THIS ACTION AND ITS RELATIONS WILL BE DELETED RECURSIVELY (TREE WILL BE PRUNED)", "Warning"):
			return
		print "Deleting " + str(self.parent.i)
		self.parent.link.delItem(self.parent.i)
		self.back()
	
	def populateExistingConnections(self):
		self.existing_connections.delete(0, END)
		for relation in self.parent.link.getRelations(self.parent.i):
			self.existing_connections.insert(END, self.parent.link.getOneID(self.parent.link.getItem(relation)))
		
	def back(self):
		print "Back"
		self.destroy()
		SLBase(self.parent)
		
	def follow(self):
		if not self.existing_connections.get(ANCHOR):
			return
		self.connection.set(self.existing_connections.get(ANCHOR))
		self.connect(True)
		self.connection.set("New element")
		
	def lightConnect(self):
		if self.connection.get() == "New element":
			self.parent.link.addRelation(self.parent.i, self.parent.link.size())
			print "Linked to index " + str(self.parent.link.size())
			self.parent.i = self.parent.link.size()
			self.load=0
			self.changeFrame(0)
			self.populateExistingConnections()
			self.updateElementList()
		else:
			self.parent.link.addRelation(self.parent.i, self.actions.index(self.connection.get()))
			print "Linked to index " + str(self.actions.index(self.connection.get()))
			self.window.save()
			self.populateExistingConnections()
		
	def connect(self, spawn):
		if self.connection.get() == "New element":
			if not spawn:
				self.parent.link.addRelation(self.parent.i, self.parent.link.size())
				print "Linked to index " + str(self.parent.link.size())
			self.parent.i = self.parent.link.size()
			self.load=0
			self.changeFrame(0)
		else:
			if not spawn:
				self.parent.link.addRelation(self.parent.i, self.actions.index(self.connection.get()))
				print "Linked to index " + str(self.actions.index(self.connection.get()))
			self.parent.i = self.actions.index(self.connection.get())
			if isinstance(self.parent.link.getItem(self.actions.index(self.connection.get())), Info):
				self.type.set("Info")
			elif isinstance(self.parent.link.getItem(self.actions.index(self.connection.get())), Speak):
				self.type.set("Speak")
			elif isinstance(self.parent.link.getItem(self.actions.index(self.connection.get())), Camera):
				self.type.set("Camera Change")
			elif isinstance(self.parent.link.getItem(self.actions.index(self.connection.get())), Movement):
				self.type.set("Movement")
			self.load = self.parent.link.getItem(self.actions.index(self.connection.get()))
			self.changeFrame(0)
			
	def updateElementList(self):
		self.next["menu"].delete(0, "end")
		self.actions = self.parent.link.getIDs()
		for action in self.actions:
			self.next["menu"].add_command(label=action, command=Tkinter._setit(self.connection, action))
		self.next["menu"].add_command(label="New element", command=Tkinter._setit(self.connection, "New element"))
		
	def changeFrame(self, something):
		print "Changed to " + self.type.get()
		try:
			self.window.destroy()
		except AttributeError:
			pass		
		if self.type.get() == "Speak":
			self.window = SpeakFrame(self, self.load)
		elif self.type.get() == "Camera Change":
			self.window = CameraFrame(self, self.load)
		elif self.type.get() == "Movement":
			self.window = MoveFrame(self, self.load)
		else:# self.type.get() == "Info":
			self.window = InfoFrame(self, self.load)
		self.save.config(command=self.window.save)
		self.populateExistingConnections()
		self.updateElementList()
			
class InfoFrame(Frame):

	def __init__(self, parent, load):
		Frame.__init__(self, master=parent)
		self.parent = parent
		self.type = StringVar(self)
		self.next = StringVar(self)
		self.load = load
		self.initUI()
		self.grid(row=1, column=0, columnspan=5)
		
	def initUI(self):		
		self.infoBox = Text(self, height=4, width=50, wrap=WORD)
		if self.load!=0:
			try:
				self.infoBox.insert(1.0, self.load.getText())
			except:
				pass
		
		self.infoBox.grid(row=1, column=0, columnspan=5)
		
			
	def save(self):
		print "Saving"
		infoSlide = Info()
		print "..."
		infoSlide.setText(self.infoBox.get(1.0, END).replace("\n", ""))
		self.parent.parent.link.addItem(infoSlide, self.parent.parent.i)
		print "Saved"
		self.parent.parent.linkstored.setLink(self.parent.parent.link, self.parent.parent.level, self.parent.parent.angle)
		self.parent.parent.linkstored.save()
		self.parent.updateElementList()
		
class SpeakFrame(Frame):
	
	def __init__(self, parent, load):
		Frame.__init__(self, master=parent)
		self.parent = parent
		self.type = StringVar(self)
		self.speakerv = StringVar(self)
		anga = StringVar(self)
		anga.set("")
		poina = StringVar(self)
		poina.set("")
		self.pointvec = []
		self.load = load
		self.pointvar = [poina]
		self.anglevec = []
		self.anglevar = [anga]
		self.addPAtIndex = 4
		self.addAAtIndex = 4
		self.initUI()
		self.grid(row=1, column=0, columnspan=5)
		
	def initUI(self):
		characs = json_reader.readCharNames()
		self.arcanas = json_reader.data_list("arcanas")
		self.arcanas.extend([""])
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		
		self.textl = Label(self, text="Text:")
		self.textl.grid(row=1, column=0)
		
		self.infoBox = Text(self, height=3, width=40, wrap=WORD)
		if self.load!=0:
			try:
				self.infoBox.insert(1.0, self.load.getText())
			except:
				pass
		self.infoBox.grid(row=1, column=1, columnspan=3, rowspan=3)
		
		self.textl = Label(self, text="Points:")
		self.textl.grid(row=2, column=4, columnspan=2)
		
		self.pointBox = Text(self, height=1, width=3)
		self.pointBox.grid(row=3, column=4)
		self.pointvec.append(self.pointBox)
		
		speaker = OptionMenu(self, self.pointvar[0], *self.arcanas)
		speaker.config(width=10)
		speaker.grid(row=3, column=5, sticky='ew')
		
		self.textl = Label(self, text="Angle:")
		self.textl.grid(row=2, column=6, columnspan=2)
		
		self.angleBox = Text(self, height=1, width=3)
		self.angleBox.grid(row=3, column=6)
		self.anglevec.append(self.angleBox)
		
		speaker = OptionMenu(self, self.anglevar[0], *self.arcanas)
		speaker.config(width=10)
		speaker.grid(row=3, column=7, sticky='ew')
		
		self.speakerl = Label(self, text="Speaker:")
		self.speakerl.grid(row=1, column=4)
		
		if self.load!=0:
			try:
				self.speakerv.set(self.load.getSpeaker())
			except:
				pass
		speaker = OptionMenu(self, self.speakerv, *characs)
		speaker.config(width=10)
		speaker.grid(row=1, column=5, sticky='ew')
		
		self.addp = Button(self, text="Add points", command=self.extendP)
		self.addp.grid(row=30, column=4, columnspan=2)
		
		self.adda = Button(self, text="Add angles", command=self.extendA)
		self.adda.grid(row=30, column=6, columnspan=2)
		
		if self.load != 0:
			try:
				first = True
				for arcana, points in self.load.getPoints().iteritems():
					if first:
						first = False
					else:
						self.extendP()
					self.pointvec[-1].insert(1.0, points)
					self.pointvar[-1].set(arcana)
				first = True
				for arcana, angle in self.load.getAngle().iteritems():
					if first:
						first = False
					else:
						self.extendA()
					self.anglevec[-1].insert(1.0, angle)
					self.anglevar[-1].set(arcana)
			except:
				pass
			
			
		
	def extendP(self):
		self.pointvec.extend([Text(self, height=1, width=3)])
		self.pointvar.extend([StringVar(self)])
		self.pointvar[-1].set("")
		self.pointvec[-1].grid(row=self.addPAtIndex, column=4)
		temp = OptionMenu(self, self.pointvar[-1], *self.arcanas)
		temp.config(width=10)
		temp.grid(row=self.addPAtIndex, column=5, sticky='ew')
		self.addPAtIndex+=1
		
	def extendA(self):
		self.anglevec.extend([Text(self, height=1, width=3)])
		self.anglevar.extend([StringVar(self)])
		self.anglevar[-1].set("")
		self.anglevec[-1].grid(row=self.addAAtIndex, column=6)
		temp=OptionMenu(self, self.anglevar[-1], *self.arcanas)
		temp.config(width=10)
		temp.grid(row=self.addAAtIndex, column=7, sticky='ew')
		self.addAAtIndex+=1
		
	def save(self):
		print "Saving"
		print "..."
		speakSlide = Speak()
		speakSlide.setText(self.infoBox.get(1.0, END).replace("\n", ""))
		speakSlide.setSpeaker(self.speakerv.get())
		for i in xrange(len(self.pointvec)):
			if(self.pointvar[i].get()!=""):
				try:
					amount = (int)(self.pointvec[i].get(1.0, END))
					speakSlide.putPoints(self.pointvar[i].get(), amount)
				except:
					popup("All Points and Angles must be integers.\nTo discard one line, set empty the text field and set the arcana to blank.", "Critical")
					print "Amount must be an integer"
		for i in xrange(len(self.anglevec)):
			if(self.anglevar[i].get()!=""):
				try:
					amount = (int)(self.anglevec[i].get(1.0, END))
					speakSlide.putAngle(self.anglevar[i].get(), amount)
				except:
					popup("All Points and Angles must be integers.\nTo discard one line, set empty the text field and set the arcana to blank.", "Critical")
					print "Amount must be an integer"
		self.parent.parent.link.addItem(speakSlide, self.parent.parent.i)
		print "Saved"
		self.parent.parent.linkstored.setLink(self.parent.parent.link, self.parent.parent.level, self.parent.parent.angle)
		self.parent.parent.linkstored.save()
		self.parent.updateElementList()
		
		
class CameraFrame(Frame):
	
	def __init__(self, parent, load):
		Frame.__init__(self, master=parent)
		self.parent = parent
		self.load = load
		self.type = StringVar(self)
		self.location = StringVar(self)
		self.initUI()
		self.grid(row=1, column=0, columnspan=5)
		
	def initUI(self):
		locations = json_reader.data_list("locations")
		self.location.set("Home")
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		
		self.textl = Label(self, text="Camera's position x:")
		self.textl.grid(row=1, column=0)
		
		self.cx = Text(self, height=1, width=3)
		self.cx.grid(row=1, column=1)
		
		self.textl = Label(self, text="Camera's position y:")
		self.textl.grid(row=2, column=0)
		
		self.cy = Text(self, height=1, width=3)
		self.cy.grid(row=2, column=1)
		
		self.textl = Label(self, text="Camera's position z:")
		self.textl.grid(row=3, column=0)
		
		self.cz = Text(self, height=1, width=3)
		self.cz.grid(row=3, column=1)
		
		self.textl = Label(self, text="Look at x:")
		self.textl.grid(row=1, column=2)
		
		self.lx = Text(self, height=1, width=3)
		self.lx.grid(row=1, column=3)
		
		self.textl = Label(self, text="Look at y:")
		self.textl.grid(row=2, column=2)
		
		self.ly = Text(self, height=1, width=3)
		self.ly.grid(row=2, column=3)
		
		self.textl = Label(self, text="Look at z:")
		self.textl.grid(row=3, column=2)
		
		self.lz = Text(self, height=1, width=3)
		self.lz.grid(row=3, column=3)
		
		self.locationl = Label(self, text="Location:")
		self.locationl.grid(row=1, column=4)
		
		locationO = OptionMenu(self, self.location, *locations)
		locationO.config(width=5)
		locationO.grid(row=1, column=5, sticky='ew')
		
		if self.load != 0:
			try:
				self.location.set(self.load.getPlace())
				cp = self.load.getCameraPosition()
				la = self.load.getLookAt()
				print cp
				print la
				self.cx.insert(1.0, cp[0])
				self.cy.insert(1.0, cp[1])
				self.cz.insert(1.0, cp[2])
				self.lx.insert(1.0, la[0])
				self.ly.insert(1.0, la[1])
				self.lz.insert(1.0, la[2])
			except:
				pass
		
			
	def save(self):
		print "Saving"
		cameraSlide = Camera()
		cameraSlide.setPlace(self.location.get())
		print "..."
		try:
			(int)(self.lx.get(1.0, END))
			(int)(self.ly.get(1.0, END))
			(int)(self.lz.get(1.0, END))
			(int)(self.cx.get(1.0, END))
			(int)(self.cy.get(1.0, END))
			(int)(self.cz.get(1.0, END))
		except:
			popup("Camera position (x, y, z) and look direction (x, y, z) must be entered as integers", "Critical")
			print "Must be an integer"
			return
		
		cameraSlide.setLookAt(((int)(self.lx.get(1.0, END)),(int)(self.ly.get(1.0, END)),(int)(self.lz.get(1.0, END))))
		cameraSlide.setCameraPosition(((int)(self.cx.get(1.0, END)),(int)(self.cy.get(1.0, END)),(int)(self.cz.get(1.0, END))))
		self.parent.parent.link.addItem(cameraSlide, self.parent.parent.i)
		print "Saved"
		self.parent.parent.linkstored.setLink(self.parent.parent.link, self.parent.parent.level, self.parent.parent.angle)
		self.parent.parent.linkstored.save()
		self.parent.updateElementList()
		
		
class MoveFrame(Frame):
	
	def __init__(self, parent, load):
		Frame.__init__(self, master=parent)
		self.parent = parent
		self.load = load
		self.type = StringVar(self)
		self.speakerv = StringVar(self)
		self.aniv = StringVar(self)
		self.initUI()
		self.grid(row=1, column=0, columnspan=5)
		
	def initUI(self):
		animations = json_reader.data_list("animations")
		characs = json_reader.readCharNames()
		self.aniv.set("Idle")
		Style().configure("TButton", padding=(0,5,0,5), background='WhiteSmoke')
		
		self.textl = Label(self, text="Go to x:")
		self.textl.grid(row=1, column=0)
		
		self.lx = Text(self, height=1, width=3)
		self.lx.grid(row=1, column=1)
		
		self.textl = Label(self, text="Go to y:")
		self.textl.grid(row=2, column=0)
		
		self.ly = Text(self, height=1, width=3)
		self.ly.grid(row=2, column=1)
		
		self.speakerl = Label(self, text="Person:")
		self.speakerl.grid(row=1, column=3)
		
		speaker = OptionMenu(self, self.speakerv, *characs)
		speaker.config(width=10)
		speaker.grid(row=1, column=4, sticky='ew')
		
		self.anil = Label(self, text="Animation:")
		self.anil.grid(row=2, column=3)
		
		ani = OptionMenu(self, self.aniv, *animations)
		ani.config(width=10)
		ani.grid(row=2, column=4, sticky='ew')
		
		if self.load != 0:
			try:
				self.aniv.set(self.load.getAnimation())
				self.speakerv.set(self.load.getSubject())
				self.lx.insert(1.0, self.load.getDestination()[0])
				self.ly.insert(1.0, self.load.getDestination()[1])
			except:
				pass
		
		
	def save(self):
		print "Saving"
		moveSlide = Movement()
		moveSlide.setSubject(self.speakerv.get())
		moveSlide.setAnimation(self.aniv.get())
		print "..."
		try:
			(int)(self.lx.get(1.0, END))
			(int)(self.ly.get(1.0, END))
		except:
			popup("Destination coordinates (x, y) must be entered as integers", "Critical")
			print "Numbers must be integers"
			return
		
		moveSlide.setDestination(((int)(self.lx.get(1.0, END)),(int)(self.ly.get(1.0, END))))
		self.parent.parent.link.addItem(moveSlide, self.parent.parent.i)
		print "Saved"
		self.parent.parent.linkstored.setLink(self.parent.parent.link, self.parent.parent.level, self.parent.parent.angle)
		self.parent.parent.linkstored.save()
		self.parent.updateElementList()
		
		
		
class Character():

	def __init__(self):
		self.name = ""
		self.desc = ""
		self.important = False
		
	def __init__(self, nameP, descP, importantP):
		self.name = nameP
		self.desc = descP
		self.important = importantP
		
	def getName(self):
		return self.name
		
	def getDesc(self):
		return self.desc
	
	def getImportant(self):
		return self.important
		
	def setName(self, pName):
		self.name = pName
		
	def setDesc(self, pDesc):
		self.desc = pDesc
		
	def setImportant(self, pImportant):
		self.important = pImportant
		
class Persona():

#	def __init__(self):
#		self.arcana = ""
#		self.name = ""
#		self.evolveName = None
#		self.level = 0
#		self.desc = ""
#		self.spellDeck = []
#		self.spellLearn = {}
#		self.stats = []
#		self.resistance = []
#		self.heritage = ()
		
	def __init__(self, name, arcana, level, desc, spellDeck, spellLearn, stats, resistance, heritage):
		self.name = name
		self.arcana = arcana
		self.level = level
		self.desc = desc
		self.spellDeck = spellDeck
		self.spellLearn = spellLearn
		self.stats = stats
		self.resistance = resistance
		self.heritage = heritage
		
	def getArcana(self):
		return self.arcana
		
	def getName(self):
		return self.name
		
	def getEvolveName(self):
		return self.evolveName
		
	def getLevel(self):
		return self.level
	
	def getDesc(self):
		return self.desc
		
	def getSpellDeck(self):
		return self.spellDeck
		
	def getSpellLearn(self):
		return self.spellLearn
		
	def getStats(self):
		return self.stats
		
	def getResistance(self):
		return self.resistance
		
	def getHeritage(self):
		return self.heritage
		
	def setArcana(self, pArcana):
		self.arcana = pArcana
		
	def setName(self, pName):
		self.name = pName
		
	def setEvolveName(self, pEvovleName):
		self.evolveName = pEvolveName
		
	def setLevel(self, pLevel):
		self.level = pLevel
	
	def setDesc(self, pDesc):
		self.desc = pDesc
		
	def setSpellDeck(self, pSpellDeck):
		self.spellDeck = pSpellDeck
		
	def setSpellLearn(self, pSpellLearn):
		self.spellLearn = pSpellLearn
		
	def setStats(self, pStats):
		self.stats = pStats
		
	def setResistance(self, pResistance):
		self.resistance = pResistance
		
	def setHeritage(self, pHeritage):
		self.heritage = pHeritage
		
class Enemy():

	def __init__(self):
		self.arcana = ""
		self.name = ""
		self.level = 0
		self.desc = ""
		self.spellDeck = []
		self.stats = []
		self.resistance = []
		
	def getArcana():
		return self.arcana
		
	def getName():
		return self.name
		
	def getLevel():
		return self.level
	
	def getDesc():
		return self.desc
		
	def getSpellDeck():
		return self.spellDeck
		
	def getStats():
		return self.stats
		
	def getResistance():
		return self.resistance
		
	def setArcana(pArcana):
		self.arcana = pArcana
		
	def setName(pName):
		self.name = pName
		
	def setLevel(pLevel):
		self.level = pLevel
	
	def setDesc(pDesc):
		self.desc = pDesc
		
	def setSpellDeck(pSpellDeck):
		self.spellDeck = pSpellDeck
		
	def setStats(pStats):
		self.stats = pStats
		
	def setResistance(pResistance):
		self.resistance = pResistance
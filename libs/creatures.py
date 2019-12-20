class Character():
    def __init__(self, nameP="", descP="", importantP=False):
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

#   def __init__(self):
#       self.arcana = ""
#       self.name = ""
#       self.evolveName = None
#       self.level = 0
#       self.desc = ""
#       self.spellDeck = []
#       self.spellLearn = {}
#       self.stats = []
#       self.resistance = []
#       self.heritage = ()

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

    def setEvolveName(self, pEvolveName):
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
# All the selfs weren't defined before whitespaces changes VERIFY
    def __init__(self):
        self.arcana = ""
        self.name = ""
        self.level = 0
        self.desc = ""
        self.spellDeck = []
        self.stats = []
        self.resistance = []

    def getArcana(self):
        return self.arcana

    def getName(self):
        return self.name

    def getLevel(self):
        return self.level

    def getDesc(self):
        return self.desc

    def getSpellDeck(self):
        return self.spellDeck

    def getStats(self):
        return self.stats

    def getResistance(self):
        return self.resistance

    def setArcana(self, pArcana):
        self.arcana = pArcana

    def setName(self, pName):
        self.name = pName

    def setLevel(self, pLevel):
        self.level = pLevel

    def setDesc(self, pDesc):
        self.desc = pDesc

    def setSpellDeck(self, pSpellDeck):
        self.spellDeck = pSpellDeck

    def setStats(self, pStats):
        self.stats = pStats

    def setResistance(self, pResistance):
        self.resistance = pResistance

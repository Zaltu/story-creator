from logictree import *
import json_reader

class SocialLink():

    def __init__(self, arcana):
        self.arcana = arcana
        self.cutscenes = {}#[level][angle]
        self.cutinfo = {}#{level_angle:"Info"}
        self.info = ""
        self.pseudoname = ""
        self.finalpersona = {} #Angle: Persona Name
        self.requiredPoints = {} #Level#:{Angle#: {'points':#, 'courage':#, 'charm':#, 'acad':#} }
        self.loadLinks()

    def setLink(self, graph, level, angle):
        self.cutscenes[str(level)+"_"+str(angle)] = graph

    def loadLinks(self):
        try:
            fullLink = json_reader.readLink(self.arcana)
            tempdic = fullLink["cutscenes"]
            print tempdic
            for id, graph in tempdic.iteritems():
                self.cutscenes[id] = MathGraph(graph["id"]).loadGraph(graph["items"])
            #if statements necessary for backwards-compatibility
            if 'pseudoname' in fullLink:
                self.pseudoname = fullLink['pseudoname']
            if 'finalpersona' in fullLink:
                self.finalpersona = fullLink['finalpersona']
            if 'requiredPoints' in fullLink:
                self.requiredPoints = fullLink['requiredPoints']
            if 'info' in fullLink:
                self.info = fullLink['info']
            if 'cutinfo' in fullLink:
                self.cutinfo = fullLink['cutinfo']
        except:
            print "No existing link"
        print self.cutscenes
        print "Loaded"

    def getLink(self, level, angle):#Not used
        try:
            return self.cutscenes.pop(str(level)+"_"+str(angle))
        except:
            print "No such link"
            return 0

    def startLink(self, level, angle):
        try:
            toreturn = self.cutscenes[(str(level)+"_"+str(angle))]
            print "Link already exists!"
        except:
            toreturn = self.cutscenes[str(level)+"_"+str(angle)] = MathGraph(self.arcana+str(level)+"_"+str(angle))
            print toreturn.items

        return toreturn

    def save(self):
        json_reader.writeLink(self)
        print "Saved to to file"

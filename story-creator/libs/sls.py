"""
Container module for the social link class.
"""
#pylint: disable=no-name-in-module
from libs.logictree import MathGraph
from libs import json_reader

class SocialLink():
    """
    Social link class. Contains all information related to each social link, as well as the cutscenes for
    each level of the link.

    :param str arcana: This Social Link's Arcana
    """
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
        """
        Set the cutscene to be played at a certain level/angle for this Social Link.

        :param MathGraph graph: cutscene
        :param int level: social link level (1-10)
        :param int angle: angle floor of this cutscene
        """
        self.cutscenes[str(level)+"_"+str(angle)] = graph

    def loadLinks(self):
        """
        Load each cutscene of this Social Link's arcana from file.
        """
        try:
            fullLink = json_reader.readLink(self.arcana)
            assert fullLink
        except AssertionError:
            print("No existing link")
            return
        tempdic = fullLink["cutscenes"]
        for cid, graph in tempdic.items():
            self.cutscenes[cid] = MathGraph(graph["id"]).loadGraph(graph["items"])

        # If statements necessary for backwards-compatibility
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
        print(self.cutscenes)
        print("Loaded")

    def startLink(self, level, angle):
        """
        Fetch the link for a given point/angle combination, creating a new one if necessary.

        :param int level: 1-10 level in the link of the cutscene
        :param int angle: angle in the link at this level for this cutscene

        :returns: cutscene at this level/angle
        :rtype: MathGraph
        """
        lid = "{level}_{angle}".format(level=level, angle=angle)
        try:
            toreturn = self.cutscenes[lid]
            print("Link already exists!")
        except KeyError:
            toreturn = self.cutscenes[lid] = MathGraph(self.arcana+lid)
            print(toreturn.items)

        return toreturn

    def save(self):
        """
        Save this Social Link (self) to file as JSON.
        """
        json_reader.writeLink(self)
        print("Saved to to file")

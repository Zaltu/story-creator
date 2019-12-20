"""
This module holds all the logic pertaining to what actions that can transpire within a cutscene represent.
"""
#pylint: disable=dangerous-default-value
def load(action):
    """
    Attempt to load a generic action dict into whatever Action type possible.

    :param dict action: action of an undefined type

    :returns: an Action object of the correct type for this undefined dict.
    :rtype: Action
    """
    obj = None
    try:
        obj = Camera()
        obj.setPlace(action["place"])
        obj.setCameraPosition(action["cameraPosition"])
        obj.setLookAt(action["lookAt"])
        return obj
    except AttributeError:
        pass
    try:
        obj = Movement()
        obj.setSubject(action["subject"])
        obj.setAnimation(action["animation"])
        obj.setDestination(action["destination"])
        return obj
    except AttributeError:
        pass
    try:
        obj = Speak()
        obj.setSpeaker(action["speaker"])
        obj.emotion = action.get('emotion', "")
        obj.setText(action["text"])
        for arcana, points in action["points"].items():
            obj.putPoints(arcana, points)
        for arcana, angle in action["angle"].items():
            obj.putAngle(arcana, angle)
        return obj
    except AttributeError:
        pass
    try:
        obj = Info()
        obj.setText(action["text"])
        return obj
    except AttributeError:
        pass


class Info():
    """
    Info Action. Represents just general info for the devs, or information for a camera or move action for
    which the coordinates are not known yet.

    :param str text: text of this info. Defaults to empty string
    """
    def __init__(self, text=""):
        self.text = text

    def setText(self, pText):
        """
        Set the text for this info action

        :param str pText: the new text for this info action
        """
        self.text = pText

    def getText(self):
        """
        Get the text of this info action

        :returns: current text
        :rtype: str
        """
        return self.text


class Speak():
    """
    Speak Action. Represents a character, including the MC, saying something in a conversation.
    May also contain flags to adjust the amount of points/angle gained toward a social link.

    :param str text: spoken text
    :param str speaker: name of person speaking this text
    :param dict points: {arcana: amount} of points to gain or lose
    :param dict angle: {arcana: amount} of angle degree to gain or lose
    :param str emotion: emotion for the sprite
    """
    def __init__(self, text="", speaker="", points={}, angle={}, emotion=""):
        self.text = text
        self.speaker = speaker
        self.points = points
        self.angle = angle
        self.emotion = emotion

    def putPoints(self, arcana, points):
        self.points[arcana] = points

    def putAngle(self, arcana, angle):
        self.angle[arcana] = angle

    def setSpeaker(self, person):
        self.speaker = person

    def setText(self, text_new):
        self.text = text_new

    def getText(self):
        return self.text

    def getSpeaker(self):
        return self.speaker

    def getPoints(self):
        return self.points

    def getAngle(self):
        return self.angle

    def display(self):
        return None#


class Camera():

    def __init__(self):
        self.place = ""
        self.cameraPosition = []
        self.lookAt = []

    def setPlace(self, placenew):
        self.place = placenew

    def setCameraPosition(self, position3):
        self.cameraPosition = position3

    def setLookAt(self, lookat3):
        self.lookAt = lookat3

    def getPlace(self):
        return self.place

    def getCameraPosition(self):
        return self.cameraPosition

    def getLookAt(self):
        return self.lookAt


class Movement():

    def __init__(self):
        self.subject = None#
        self.destination = ()
        self.animation = None#

    def setSubject(self, person):
        self.subject = person

    def setDestination(self, tuple):
        self.destination = tuple

    def setAnimation(self, aniname):
        self.animation = aniname

    def getSubject(self):
        return self.subject

    def getDestination(self):
        return self.destination

    def getAnimation(self):
        return self.animation

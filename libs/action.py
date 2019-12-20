def load(action):
    o = None
    try:
        o = Camera()
        o.setPlace(action["place"])
        o.setCameraPosition(action["cameraPosition"])
        o.setLookAt(action["lookAt"])
        return o
    except:
        pass
    try:
        o = Movement()
        o.setSubject(action["subject"])
        o.setAnimation(action["animation"])
        o.setDestination(action["destination"])
        return o
    except:
        pass
    try:
        o = Speak()
        o.setSpeaker(action["speaker"])
        if 'emotion' in action:
            o.emotion = action['emotion']
        o.setText(action["text"])
        for arcana, points in action["points"].items():
            o.putPoints(arcana, points)
        for arcana, angle in action["angle"].items():
            o.putAngle(arcana, angle)
        return o
    except:
        pass
    try:
        o = Info()
        o.setText(action["text"])
        return o
    except:
        pass


class Info():

    def __init__(self):
        self.text = ""

    def setText(self, pText):
        self.text = pText

    def getText(self):
        return self.text


class Speak():

    def __init__(self):
        self.text = ""
        self.speaker = ""
        self.points = {}
        self.angle = {}
        self.emotion = ""

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

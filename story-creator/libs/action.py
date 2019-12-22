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
    except KeyError:
        pass
    try:
        obj = Movement()
        obj.setSubject(action["subject"])
        obj.setAnimation(action["animation"])
        obj.setDestination(action["destination"])
        return obj
    except KeyError:
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
    except KeyError:
        pass
    try:
        obj = Info()
        obj.setText(action["text"])
        return obj
    except KeyError:
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
        """
        Populate a certain arcana's point delta.

        :param str arcana: social link arcana to modify
        :param int points: delta points
        """
        self.points[arcana] = points

    def putAngle(self, arcana, angle):
        """
        Populate a certain arcana's angle delta.

        :param str arcana: social link arcana to modify
        :param int angle: delta angle
        """
        self.angle[arcana] = angle

    def setSpeaker(self, person):
        """
        Set the speaker of this speak action.

        :param str person: person who speaks
        """
        self.speaker = person

    def setText(self, text_new):
        """
        Set the text spoken.

        :param str text_new: new text
        """
        self.text = text_new

    def getText(self):
        """
        Get the text of this speak action.

        :returns: text
        :rtype: str
        """
        return self.text

    def getSpeaker(self):
        """
        Get the speaker of this text

        :returns: person saying the text
        :rtype: str
        """
        return self.speaker

    def getPoints(self):
        """
        Get the amount of points changed per social link by arcana from this speak action.

        :returns: Total point delta
        :rtype: dict
        """
        return self.points

    def getAngle(self):
        """
        Get the amount of angle changed per social link by arcana from this speak action.

        :returns: Total angle delta
        :rtype: dict
        """
        return self.angle


class Camera():
    """
    Camera actions represent the movement of the game camera to a certain position in a certain environment,
    and looking towards a certain point.

    :param str place: env in which the camera should be
    :param list cameraPosition: xyz coordinates of the center of the camera itself
    :param list lookAt: xyz coordinates that the camera's focus should be centered on
    """
    def __init__(self, place="", cameraPosition=[], lookAt=[]):
        self.place = place
        self.cameraPosition = cameraPosition
        self.lookAt = lookAt

    def setPlace(self, placenew):
        """
        Set the place (env) the camera should be.

        :param str placenew: place name
        """
        self.place = placenew

    def setCameraPosition(self, position3):
        """
        Set the camera object center's position.

        :param list position3: xyz camera coordinates
        """
        self.cameraPosition = position3

    def setLookAt(self, lookat3):
        """
        Set position that the camera should be focues on.

        :param list lookat3: xyz look-at coordinates
        """
        self.lookAt = lookat3

    def getPlace(self):
        """
        Get the camera's place (env)/

        :returns: place name
        :rtype: str
        """
        return self.place

    def getCameraPosition(self):
        """
        Get the camera object's center's coordinates

        :returns: camera position
        :rtype: list[float]
        """
        return self.cameraPosition

    def getLookAt(self):
        """
        Get the coordinates the camera should be looking at.

        :returns: camera's focus location
        :rtype: list[float]
        """
        return self.lookAt


class Movement():
    """
    Movement actions represent moving a certain scene object to a new set of coordinates using a certain
    animation (or none).

    :param str subject: name of the subject to move
    :param list destination: xy coordinates on the floor plan to move to
    :param str animation: the animation to use during the movement
    """
    def __init__(self, subject=None, destination=(), animation=None):
        self.subject = subject
        self.destination = destination
        self.animation = animation

    def setSubject(self, person):
        """
        Set the subject to be moved

        :param str person: subject name
        """
        self.subject = person

    def setDestination(self, xy):
        """
        xy coordinates the movement should leave the subject at.

        :param tuple xy: xy coordinates based on the floor plan
        """
        self.destination = xy

    def setAnimation(self, aniname):
        """
        Set the animation to be used during the move.

        :param str aniname: name of the animation
        """
        self.animation = aniname

    def getSubject(self):
        """
        Get the subject moved.

        :returns: subject name
        :rtype: str
        """
        return self.subject

    def getDestination(self):
        """
        Get the final destination of the movement.

        :returns: xy floor plan coordinates
        :rtype: tuple
        """
        return self.destination

    def getAnimation(self):
        """
        Get the animation used for this move.

        :returns: name of animation used
        :rtype: str
        """
        return self.animation

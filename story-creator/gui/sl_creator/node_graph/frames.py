"""
Nodes corresponding to the View Frames of the old implementation in story-creator
"""
from NodeGraphQt import BaseNode

from libs import json_reader


class PersonaXNode(BaseNode):
    """
    Sets identifier.
    Hyper-OO ahoy!
    """
    # Node identifier
    __identifier__ = "personax"


class InfoNode(PersonaXNode):
    """
    Node implementation of InfoFrame

    :param Info info: the info action this node represents
    """
    # Default node name
    NODE_NAME = "InfoNode"

    def __init__(self, info):
        super().__init__()
        self.info = info

        # InfoFrame has only one text property.
        self.text = self.add_text_input("info_text", info.text)

        ## Add IO
        # Any number of previous nodes can connect.
        self.add_input("Previous", multi_input=True)
        # Can only connect to a single output.
        self.add_output("Next", multi_output=False)

class SpeakNode(PersonaXNode):
    """
    Node implementation of SpeakFrame

    :param Speak speak: the speak action this node represents
    """
    # Default node name
    NODE_NAME = "SpeakNode"

    def __init__(self, speak):
        super().__init__()
        self.speak = speak

        ## SpeakFrame properties
        self.text = self.add_text_input("text", "Text", speak.text)
        self.chars = self.add_combo_menu("chars", "Speaker", items=json_reader.readCharNames())
        self.chars.value = speak.speaker
        self.emo = self.add_combo_menu("emotions", "Emotion", items=json_reader.data_list("sprite_emotions"))
        self.emo.value = speak.emotion
        # Handling of more points/angle/arcana through buttons and tabs TODO

        ## Add IO
        # Any number of previous nodes can connect.
        self.add_input("Previous", multi_input=True)
        # Connects to all choices
        self.add_output("Next", multi_output=True)


class CameraNode(PersonaXNode):
    """
    Node implementation of CameraFrame

    :param Camera camera: camera action this node represents
    """
    # Default node name
    NODE_NAME = "CameraNode"

    def __init__(self, camera):
        super().__init__()
        self.camera = camera

        ## CameraFrame properties
        self.place = self.add_combo_menu("place", "Location", json_reader.data_list("locations"))
        self.place.value = camera.place
        self.cx = self.add_text_input("cx", "Camera's Position x", camera.position[0])
        self.cy = self.add_text_input("cy", "Camera's Position y", camera.position[1])
        self.cz = self.add_text_input("cz", "Camera's Position z", camera.position[2])
        self.lx = self.add_text_input("lx", "Look at x", camera.lookAt[0])
        self.ly = self.add_text_input("ly", "Look at y", camera.lookAt[1])
        self.lz = self.add_text_input("lz", "Look at z", camera.lookAt[2])

        ## Add IO
        # Any number of previous nodes can connect.
        self.add_input("Previous", multi_input=True)
        # Can only connect to a single output.
        self.add_output("Next", multi_output=False)


class MoveNode(PersonaXNode):
    """
    Node implementation of MoveFrame

    :param Movement move: move action this node represents
    """
    # Default node name
    NODE_NAME = "MoveNode"

    def __init__(self, move):
        super().__init__()
        self.move = move

        ## MoveFrame properties
        self.lx = self.add_text_input("lx", "Go to x", move.destination[0])
        self.ly = self.add_text_input("ly", "Go to y", move.destination[1])
        self.persona = self.add_combo_menu("person", "Person", items=json_reader.readCharNames())
        self.person.value = move.subject
        self.anim = self.add_combo_menu("anim", "Animation", items=json_reader.data_list("animations"))
        self.anim.value = move.animation

        ## Add IO
        # Any number of previous nodes can connect.
        self.add_input("Previous", multi_input=True)
        # Can only connect to a single output.
        self.add_output("Next", multi_output=False)

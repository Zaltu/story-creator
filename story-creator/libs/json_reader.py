"""
Utility to facilitate loading from and saving to JSON files.
"""
import os
import sys
from glob import glob
import json


def buildPath(filename):
    """
    Build the absolute path to the filename from the system, taking into account whether a dist version of
    the application is running or not.

    :param str filename: path to a file or file marker (*.json) relative to the top-level of this
                         application's package

    :returns: absolute path to file(s)
    :rtype: str
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), str(filename))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../", filename))


def writeLink(link):
    """
    Write a social link to a file on disk.
    Saves to data/{link_name}/{arcana}_link.json

    :param SocialLink link: social link to write.
    """
    with open(buildPath('data/' + link.arcana + '_link.json'), 'w') as outfile:
        json.dump(link, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    outfile.close()


def readLink(arcana):
    """
    Loads a social link from a file on disk.

    :param str arcana: arcana who's social link to load

    :return: social link json data
    :rtype: list
    """
    try:
        with open(buildPath('data/' + arcana + '_link.json')) as json_data:
            array = json.load(json_data)
        json_data.close()
        return array
    except FileNotFoundError:
        return {}


def readArcDesc(arcana):
    """
    Fetch the description of a given arcana

    :param str arcana: arcana's description to fetch

    :returns: arcana description
    :rtype: str
    """
    with open(buildPath('int/' + 'arcanaDescription.json')) as json_data:
        array = json.load(json_data)
    json_data.close()
    return array[arcana]


def writeOne(entity, creatureType):
    """
    Writes a single entity to disk.
    (Generally used for Personas and Characters)
    data/{type}/{name}.json

    :param Creature entity: entity to write
    :param str creatureType: type of creature, for filepath purposes
    """
    with open(buildPath('data/%s/%s.json' % (creatureType, entity.getName())), 'w') as outfile:
        json.dump(entity.__dict__, outfile, indent=4)
    outfile.close()


def readOne(name, creatureType):
    """
    Reads a single entity from disk.

    :param str name: name of creature to load
    :param str creatureType: type of the creature

    :returns: json load of the creature
    :rtype: dict
    """
    with open(buildPath('data/%s/%s.json' % (creatureType, name))) as json_data:
        entity = json.load(json_data)
    json_data.close()
    return entity


def readPerNames():
    """
    Read the caching file containing the names of all saved Personas.

    :returns: names of all saved Personas
    :rtype: list[str]
    """
    chars = glob(buildPath('data/pers/*.json'))
    return [os.path.basename(charname.split('.')[0]) for charname in chars]


def deleteChar(name):
    """
    Delete the file of a single character.

    :param str name: name of character to delete
    """
    os.remove(buildPath('data/chars/' + name + '.json'))


def deletePer(name):
    """
    Delete the file of a single Persona.

    :param str name: name of Persona to delete
    """
    os.remove(buildPath('data/pers/' + name + '.json'))


def readCharNames():
    """
    Read the caching file containing the names of all saved characters.

    :returns: names of all saved characters
    :rtype: list[str]
    """
    chars = glob(buildPath('data/chars/*.json'))
    return [os.path.basename(charname.split('.')[0]) for charname in chars]


def data_list(fetch):
    """
    Fetch one of our data lists that are saved in the general data file.

    :param str fetch: name of the list to fetch (dict index)

    :returns: entry in the general data file at the requested key
    :rtype: list|dict
    """
    with open(buildPath('int/' + 'data.json')) as json_data:
        temp = json.load(json_data)
    json_data.close()
    data = temp[fetch]
    return data

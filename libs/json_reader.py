import os
import sys
from glob import glob
import json
from libs.creatures import Character


def buildPath(fileName):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), str(fileName))
    return fileName


def writeLink(link):
    with open(buildPath('data/' + link.arcana + '_link.json'), 'w') as outfile:
        json.dump(link, outfile, default=lambda o: o.__dict__, sort_keys=True)
    outfile.close()


def readLink(arcana):
    try:
        with open(buildPath('data/' + arcana + '_link.json')) as json_data:
            array = json.load(json_data)
        json_data.close()
        return array
    except Exception as e:
        print e
        return {}


def readArcDesc(arcana):
    with open(buildPath('int/' + 'arcanaDescription.json')) as json_data:
        array = json.load(json_data)
    json_data.close()
    return array[arcana]


def writeOne(character):
    with open(buildPath('data/chars/' + character.getName() + '.json'), 'w') as outfile:
        json.dump(character.__dict__, outfile)
    outfile.close()


def writeOneP(persona):
    with open(buildPath('data/pers/' + persona.getName() + '.json'), 'w') as outfile:
        json.dump(persona.__dict__, outfile)
    outfile.close()


def readOne(name):
    with open(buildPath('data/chars/' + name+'.json')) as json_data:
        characterL = json.load(json_data)
    json_data.close()
    return Character(characterL["name"], characterL["desc"], characterL["important"])


def readP(fetch):
    with open(buildPath('data/pers/' + fetch+".json")) as json_data:
        persona = json.load(json_data)
    json_data.close()
    return persona


def readPerNames():
    chars = glob(buildPath('data/pers/*.json'))
    return [charname.split('.')[0].split("/")[-1] for charname in chars]


def deleteChar(name):
    os.remove(buildPath('data/chars/' + name + '.json'))


def deletePer(name):
    os.remove(buildPath('data/pers/' + name + '.json'))


def readCharNames():
    chars = glob(buildPath('data/chars/*.json'))
    return [charname.split('.')[0].split("/")[-1] for charname in chars]


def data_list(fetch):
    with open(buildPath('int/' + 'data.json')) as json_data:
        temp = json.load(json_data)
    json_data.close()
    data = temp[fetch]
    noU = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        noU.append(item)
    return noU

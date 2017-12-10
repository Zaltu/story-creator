from creatures import Character
import os
import sys
import json


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
        print(e)
        return {}


def readArcDesc(arcana):
    with open(buildPath('int/' + 'arcanaDescription.json')) as json_data:
        array = json.load(json_data)
    json_data.close()
    return array[arcana]


def writeOne(character):
    with open(buildPath('data/' + character.getName() + '.json'), 'w') as outfile:
        json.dump(character.__dict__, outfile)
    outfile.close()
    writeCharNames(character.getName())


def writeOneP(persona):
    with open(buildPath('data/' + persona.getName() + '.json'), 'w') as outfile:
        json.dump(persona.__dict__, outfile)
    outfile.close()
    writePerNames(persona.getName())


def readOne(name):
    with open(buildPath('data/' + name+'.json')) as json_data:
        characterL = json.load(json_data)
    json_data.close()
    return Character(characterL["name"], characterL["desc"], characterL["important"])


def readP(fetch):
    with open(buildPath('data/' + fetch+".json")) as json_data:
        persona = json.load(json_data)
    json_data.close()
    return persona


def writeCharNames(name):
    list = readCharNames()
    if name in list:
        return
    list.append(name)
    with open(buildPath('int/' + 'chars.json'), 'w') as outfile:
        json.dump(list, outfile)
    outfile.close()


def writePerNames(name):
    list = readPerNames()
    if name.encode('utf-8') in list:
        return
    list.append(name.encode('utf-8'))
    with open(buildPath('int/' + 'pers.json'), 'w') as outfile:
        json.dump(list, outfile)
    outfile.close()


def readPerNames():
    with open(buildPath('int/' + 'pers.json')) as json_data:
        names = json.load(json_data)
    json_data.close()
    return names


def deleteChar(name):
    list = readCharNames()
    list.remove(name)
    with open(buildPath('int/' + 'chars.json'), 'w') as outfile:
        json.dump(list, outfile)
    outfile.close()
    os.remove(buildPath('data/' + name + '.json'))


def deletePer(name):
    list = readPerNames()
    list.remove(name)
    with open(buildPath('int/' + 'pers.json'), 'w') as outfile:
        json.dump(list, outfile)
    outfile.close()
    os.remove(buildPath('data/'+name + '.json'))


def readCharNames():
    with open(buildPath('int/' + 'chars.json')) as json_data:
        names = json.load(json_data)
    json_data.close()
    return names


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

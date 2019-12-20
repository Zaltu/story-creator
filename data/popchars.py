from shotgun_api3 import Shotgun
from glob import glob
import json

SCRIPT_NAME = 'Samuel - API'
SCRIPT_KEY = ''
sg = Shotgun("https://objeus.shotgunstudio.com", SCRIPT_NAME, SCRIPT_KEY)

echars = sg.find('CustomEntity06', [], ['code'])
efiles = sg.find('Attachment', [['attachment_links', 'type_is', 'CustomEntity06']], ['attachment_links'])
efilenames = {}
for efile in efiles:
	efilenames[efile['attachment_links'][0]['name']] = efile['id']
print efilenames
enames = {}
for echar in echars:
	enames[echar['code']] = echar
print enames

chars = glob('chars/*.json')
for char in chars:
	with open(char) as json_data:
		temp = json.load(json_data)
	json_data.close()
	data = {
			'code':temp['name'],
			'description':temp['desc']
	}
	if temp['name'] not in enames:
		data['project'] = {'type':'Project', 'id':70}
		id = sg.create('CustomEntity06', data, ['id'])['id']
	else:
		if temp['name'] in efilenames:
			sg.delete('Attachment', efilenames[temp['name']])
		id = sg.update('CustomEntity06', enames[temp['name']]['id'], data)['id']
	sg.upload('CustomEntity06', id, char, 'sg_json')
from shotgun_api3 import Shotgun
from glob import glob
import json

SCRIPT_NAME = 'Samuel - API'
SCRIPT_KEY = ''
sg = Shotgun("https://objeus.shotgunstudio.com", SCRIPT_NAME, SCRIPT_KEY)

epers = sg.find('CustomEntity07', [], ['code'])
efiles = sg.find('Attachment', [['attachment_links', 'type_is', 'CustomEntity07']], ['attachment_links'])
efilenames = {}
for efile in efiles:
	efilenames[efile['attachment_links'][0]['name']] = efile['id']
print efilenames
enames = {}
for eper in epers:
	enames[eper['code']] = eper
print enames

pers = glob('pers/*.json')
for per in pers:
	with open(per) as json_data:
		temp = json.load(json_data)
	json_data.close()
	data = {
			'code':temp['name'],
			'description':temp['desc'],
			'sg_arcana':temp['arcana'],
			'sg_level':(int)(temp['level']),
			'sg_json':None
	}
	if temp['name'] not in enames:
		data['project'] = {'type':'Project', 'id':70}
		id = sg.create('CustomEntity07', data, ['id'])['id']
	else:
		id = sg.update('CustomEntity07', enames[temp['name']]['id'], data)['id']
		if temp['name'] in efilenames:
			sg.delete('Attachment', efilenames[temp['name']])
	sg.upload('CustomEntity07', id, per, 'sg_json')
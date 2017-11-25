import json
#import json_reader

# def writeArray(array):
#	a = [0, 1, 2, 3]
	# with open('temp.json', 'w') as outfile:
		# json.dump(array, outfile)
	# outfile.close()

def readArray():
	with open('test.json') as json_data:
		array = json.load(json_data)
	json_data.close()
	print array["Fool"]
	print array["Magician"]
	for item in array:
		print item
	# toRet = []
	# for item in array:
		# toRet.append(item["name"])
	# return toRet
	#print array
	#noU = []
	#for item in array:
	#	if isinstance(item, unicode):
	#		item = item.encode('utf-8')
	#	noU.append(item)
	#print noU
	#for persona in personas:
	#	if persona["name"] == name:
	#		return persona["level"]

#writeArray()
readArray()


#print json_reader.arcana_names()

#tval = {"Yes":1, "No":2}
#cwt = CJR()
#cwt.writeOne(tval)
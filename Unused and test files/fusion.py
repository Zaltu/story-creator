#Simple two-way fusion with same-arcana debuff feature
import json_reader

def fuse(name1, name2):	
	newlevel = ( json_reader.base_level_of(name1) + json_reader.base_level_of(name2) )/2 + 1
	newarcana = json_reader.read_combos(name1, name2)
	return json_reader.fused_persona(newarcana, newlevel)

#def fuse((a1, lowlev), a2, a3):
#	name = fuse(a1, a2, lowlev)
	

def getPersona(name):
	return "Persona's map"

print fuse("Seraph", "Seraph")
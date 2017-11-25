#This is the basic social link containment class

class LinkMap():
	
	def __init__(self):
		self.action_map = {}
	
	
	def addValue(action):
		action_map[action.hash()] = action
	
	def getAction(hash):
		return action_map[hash]
	
	def removeValue(hash, treedel):
		multiplelocations = False
		if treedel:
			for relation in action_map[hash].getRelations()
				for ah, a in action_map.iteritems():
					if a.hasRelation(relation) and a.hash() is not hash:
						multiplelocations = True
					if not multiplelocations
						removeValue(ah, True)
		
		del  action_map[hash]
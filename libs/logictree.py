from libs import action

class MathGraph:

    def __init__(self, name):
        self.id = name
        self.items = DynamicList()

    def loadGraph(self, value):
        index = 0
        jndex = 0
        for io in value:
            for jo in io:
                if jndex == 0:
                    self.addItem(action.load(jo), index)
                else:
                    self.addRelation(index, ((int)(jo)))
                jndex += 1
            index += 1
            jndex = 0
        return self

    def size(self):
        return len(self.items)

    def setFirst(self, item):#Not useful (index 0 always first element). Only useful if I do a full overhaul to a pure hashmap structure (which at this point won't happen)
        self.first = item

    def getIDs(self):#safe but UGLY AF
        temp = []
        for e in self.items:
            ret = self.getOneID(e[0])
            if ret is None:
                break
            if ret not in temp:
                temp.append(ret)
            else:
                temp.append(ret+str(len(temp)))
        return temp

    def getOneID(self, element):#safe but UGLY AF
        temp = None
        if isinstance(element, action.Info) or isinstance(element, action.Speak):
            temp = element.text
        elif isinstance(element, action.Camera):
            temp = element.place
        elif isinstance(element, action.Movement):
            temp = element.subject
        return temp

    def getItem(self, index):
        return self.items[index][0]

    def getRelations(self, index):
        if len(self.items) != 0:
            return self.items[index][1:len(self.items[index])]
        else:
            return []

    def addItem(self, action, index):
        if not isinstance(self.items[index], DynamicList):
            self.items[i] = DynamicList()
        self.items[index][0] = action

    def addRelation(self, i, j):
        if j not in self.items[i]:
            self.items[i].append(j)

    def delRelation(self, i, j):
        self.items[i].remove(j)
        jfound = False
        print(self.items[i])
        for itemRelation in self.items:
            if j in itemRelation:
                jfound = True
        if not jfound:
            self.delItem(j)

    def delItem(self, i):
        for relation in self.items[i][1:len(self.items[i])]:
            self.delRelation(i, relation)
        for itemRelation in self.items:
            if i in itemRelation:
                itemRelation.remove(i)      
        self.items.pop(i)

    def subTree(self, i, processed=set()):
        countx = 0
        county = 0
                
        UD = []
        ignore = []
        if i != 0:
            ignore.append(0)#We don't want to consider anything solely accessible by root to be "part of the subtree". Root is a unique case.
        fullsubtree = self.ywaysfromi(i, processed)
        print(fullsubtree)
        for j in fullsubtree:
            if j not in ignore:
                for item in fullsubtree:
                    if item not in ignore and j in self.items[item]:
                        print("[Subtree] Link to " + str(j) + " at index " + str(item))
                        county += 1
                for item in self.items:
                    if j in item:
                        print("[Full Tree] Link to " + str(j) + " at index " + str(self.items.index(item)))
                        countx += 1
                print("Is it unique?")
                print(str(county) + " relations in the subtree")
                print(str(countx) + " relations in the full tree")
                if county == countx:
                    print("Yes")
                    UD.append(j)
                else:
                    if j != i:
                        ignore.append(j)
                        print("Removing " +str(j) + " from future checks in subtree")
                        for ignoresub in self.ywaysfromi(j):
                            if ignoresub not in ignore:
                                ignore.append(ignoresub)
                                print("Removing " +str(ignoresub) + " from future checks in subtree")
            county = 0
            countx = 0

        UD.append(i)
        if 0 in UD and i != 0:
            UD.pop(0)

        return UD

        """
        LOGIC:
        Find the subtree of element at index i
        Great, but we need to ensure that each element in the subtree is uniquely dependant on i, so:
        for each element j in the subtree, compare:
            The number of ways to reach j in the subtree
        to
            The global number of ways to reach j
        If the number of global ways to reach j is equal to the number of ways in the subtree, that means every
        single way of reaching j is encompassed by the subtree, thus element j is uniquely dependant on element i.

        county = Number of ways to reach j in the subtree
        countx = Global number of ways to reach j
        UD = Uniquely Dependant. List containing element indexes of uniquely dependant elements.
        ignore = Special case:
            When perusing the subtree, if a non-unique index is found we can be sure that any elements accessible
            from that index are also not unique. Thus, we need to remove them from further consideration when we
            check whether an element is accessible from the subtree.
            Since the root of the tree is the starting point, if we are not considering the 'subtree of root' (which
            would be the entire tree) then we must ignore any unique dependancies passing through root.

        Returns:
            UD: A list of the indexes of every element uniquely depedant on i, including i.
        """

    def ywaysfromi(self, i, processed=set()):
        sub = processed
        if i not in sub:
            sub = sub | set([i])
            for relation in self.items[i][1:len(self.items[i])]:
                sub = sub | self.ywaysfromi(relation, sub)
        return sub


class DynamicList(list):#Needs relocating (theoretically)

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))


    def __setslice__(self, i, j, seq):
        return self.__setitem__(slice(i, j), seq)


    def __delslice__(self, i, j):
        return self.__delitem__(slice(i, j))


    def _resize(self, index):
        n = len(self)
        if isinstance(index, slice):
            m = max(abs(index.start), abs(index.stop))
        else:
            m = index + 1
        if m > n:
            self.extend([self.__class__() for i in range(m - n)])


    def __getitem__(self, index):
        self._resize(index)
        return list.__getitem__(self, index)


    def __setitem__(self, index, item):
        self._resize(index)
        if isinstance(item, list):
            item = self.__class__(item)
        list.__setitem__(self, index, item)

"""
This module defines the data structure used to handle the unidirectional, multi-input, potentially repeating
graphs that are social links.
"""
#pylint: disable=no-name-in-module
from libs import action

class MathGraph:
    """
    Data struture representing a unidirectional, multi-input, potentially repeating graph.

    - Unidirectional: each node in the graph may only lead to a single other node.
    - Multi-input: many nodes may lead to the same node.
    - Potentially repeating: the graph may contain loops.

    :param str name: id of the graph (for PX, social link arcana)
    """
    def __init__(self, name):
        self.id = name
        self.items = DynamicList()

    def loadGraph(self, value):
        """
        Load a dict (JSON) of a saved graph as a MathGraph object.
        See SocialLink doc in libs/sls.py for format.

        :param dict value: loaded dict

        :returns: self, once the graph as been loaded.
        :rtype: MathGraph
        """
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
        """
        Get the number of nodes in the graph.
        (Number of actions in this social link cutscene.)

        :returns: number of nodes
        :rtype: int
        """
        return len(self.items)

    def getIDs(self):  # Safe but UGLY AF
        """
        Get the IDs of every node in the graph, iteratively.

        :returns: IDs of all graph nodes
        :rtype: list
        """
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

    def getOneID(self, element):  # Safe but UGLY AF TODO
        """
        Get the ID of a specific node in the graph.
        Does an ugly check to see what type of PX cutscene action the node is and loads the ID based on that.

        :param Action element: action of unknown type to get ID of

        :returns: action ID
        :rtype: str
        """
        temp = None
        if isinstance(element, (action.Info, action.Speak)):
            temp = element.text
        elif isinstance(element, action.Camera):
            temp = element.place
        elif isinstance(element, action.Movement):
            temp = element.subject
        return temp

    def getItem(self, index):
        """
        Get the node at a given index.

        :param int index: index at which to fetch the node

        :returns: action at the given index
        :rtype: Action
        """
        return self.items[index][0]

    def getRelations(self, index):
        """
        Get the relationships of whatever Action is located at a specific index.

        :param int index: index of an Action

        :returns: Relational index(es)
        :rtype: list
        """
        if len(self.items) != 0:
            return self.items[index][1:len(self.items[index])]
        return []

    def addItem(self, act, index):
        """
        Sets an action to a certain index, overwriting what is currently there.

        :param Action act: Action to set
        :param int index: index at which to set
        """
        if not isinstance(self.items[index], DynamicList):
            self.items[index] = DynamicList()
        self.items[index][0] = act

    def addRelation(self, i, j):
        """
        Add an additional relation to a certain index.

        :param int i: index of item to add a relationship to
        :param int j: index the Action at i should link to
        """
        if j not in self.items[i]:
            self.items[i].append(j)

    def delRelation(self, i, j):
        """
        Remove a relationship at Action i.
        Also removes any the item at index j if no other node in the graph leads to j.

        :param int i: index at which to remove a relationship
        :param int j: relationship index to remove
        """
        self.items[i].remove(j)
        jfound = False
        for itemRelation in self.items:
            if j in itemRelation:
                jfound = True
        if not jfound:
            self.delItem(j)

    def delItem(self, i):
        """
        Deletes the item at a given index.
        Also recusively removes the relationships, which may trigger further item removals.
        Used to delete a unique subtree.

        :param int i: index of Action to remove
        """
        for relation in self.items[i][1:len(self.items[i])]:
            self.delRelation(i, relation)
        for itemRelation in self.items:
            if i in itemRelation:
                itemRelation.remove(i)
        self.items.pop(i)

    def subTree(self, i):
        """
        Find the subtree of element at index i
        Great, but we need to ensure that each element in the subtree is uniquely dependant on i, so:
        for each element j in the subtree, compare:
            The number of ways to reach j in the subtree
        to
            The global number of ways to reach j
        If the number of global ways to reach j is equal to the number of ways in the subtree, that means
        every single way of reaching j is encompassed by the subtree, thus element j is uniquely dependant on
        element i.

        county = Number of ways to reach j in the subtree
        countx = Global number of ways to reach j
        UD = Uniquely Dependant. List containing element indexes of uniquely dependant elements.
        ignore = Special case:
            When perusing the subtree, if a non-unique index is found we can be sure that any elements
            accessible from that index are also not unique. Thus, we need to remove them from further
            consideration when we check whether an element is accessible from the subtree.
            Since the root of the tree is the starting point, if we are not considering the 'subtree of root'
            (which would be the entire tree) then we must ignore any unique dependancies passing through root.

        :param int i: element of which to find the unique subtree

        :returns: UD, a list of the indexes of every element uniquely depedant on i, including i.
        :rtype: list
        """
        countx = 0
        county = 0

        ud = []
        ignore = []
        processed = set()
        if i != 0:
            # We don't want to consider anything solely accessible by root to be "part of the subtree".
            # Root is a unique case.
            ignore.append(0)
        fullsubtree = self.ywaysfromi(i, processed)
        for j in fullsubtree:
            if j not in ignore:
                for item in fullsubtree:
                    if item not in ignore and j in self.items[item]:
                        county += 1
                for item in self.items:
                    if j in item:
                        countx += 1
                if county == countx:
                    ud.append(j)
                else:
                    if j != i:
                        ignore.append(j)
                        for ignoresub in self.ywaysfromi(j):
                            if ignoresub not in ignore:
                                ignore.append(ignoresub)
            county = 0
            countx = 0

        ud.append(i)
        if 0 in ud and i != 0:
            ud.pop(0)

        return ud

    def ywaysfromi(self, i, processed=set()):  #pylint: disable=dangerous-default-value
        """
        Recusively find all nodes that are accessible in any number of steps from a certain node.

        :param int i: index of node to find subtree of
        :param set processed: set of already processed nodes, to avoid duplication or infinite recursion

        :returns: the full subtree of the given node
        :rtype: set
        """
        sub = processed
        if i not in sub:
            sub = sub | set([i])
            for relation in self.items[i][1:len(self.items[i])]:
                sub = sub | self.ywaysfromi(relation, sub)
        return sub


class DynamicList(list):#Needs relocating (theoretically)
    """
    Copy-pasted scalable array off the internet. Can't remember why I didn't just do something smarter
    myself.
    """
    def __getslice__(self, i, j):
        """
        Force slice to pass by overloaded getitem.

        :param int i: slice start
        :param in j: slice end

        :returns: self sliced to ij delimiters
        :rtype: DynamicList
        """
        return self.__getitem__(slice(i, j))


    def __setslice__(self, i, j, seq):
        """
        Force slice to pass by overloaded setitem.

        :param int i: slice start
        :param in j: slice end
        :param list seq: sequence to set to

        :returns: self with sliced to ij delimiters replaced
        :rtype: DynamicList
        """
        return self.__setitem__(slice(i, j), seq)


    def __delslice__(self, i, j):
        """
        Force slice to pass by overloaded delitem.

        :param int i: slice start
        :param in j: slice end

        :returns: self with ij sliced out
        :rtype: DynamicList
        """
        return self.__delitem__(slice(i, j))


    def _resize(self, index):
        """
        Resizes self as requested by a setitem.
        Very stupid.

        :param int index: index reference for how far self needs to be rezised
        """
        #pylint: disable=invalid-name
        n = len(self)
        if isinstance(index, slice):
            m = max(abs(index.start), abs(index.stop))
        else:
            m = index + 1
        if m > n:
            self.extend([self.__class__() for i in range(m - n)])
        #pylint: enable=invalid-name

    def __getitem__(self, index):
        """
        Make sure to always be able to serve a requested index using _resize.

        :param int index: list index

        :return: guarenteed to return without error self at index
        :rtype: object
        """
        self._resize(index)
        return list.__getitem__(self, index)


    def __setitem__(self, index, item):
        """
        Make sure to always be able to set a value in self for a given index.

        :param int index: index to set
        :param object item: object to put at index
        """
        self._resize(index)
        if isinstance(item, list):
            item = self.__class__(item)
        list.__setitem__(self, index, item)

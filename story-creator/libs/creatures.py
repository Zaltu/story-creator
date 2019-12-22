"""
This module defines data classes for "living" subjects within PX.
"""
class Character():
    """
    The Character class represents a character that can appear in the game, or any entity which could have
    dialog or a personality attached to it (such as a narrator or fourth-wall-breaking text).

    :param str name: the name of the Character
    :param str desc: a description of the character
    :param bool important: whether the character requires artwork or additional media. Defaults to False
    """
    def __init__(self, name="", desc="", important=False):
        self.name = name
        self.desc = desc
        self.important = important

    def getName(self):
        """
        Get the character's name.

        :returns: name
        :rtype: str
        """
        return self.name

    def getDesc(self):
        """
        Get the character's description.

        :returns: description
        :rtype: str
        """
        return self.desc

    def getImportant(self):
        """
        Get if the character is important/requires additional media.

        :returns: important flag
        :rtype: bool
        """
        return self.important

    def setName(self, name):
        """
        Set the name of the character.

        :param str name: name
        """
        self.name = name

    def setDesc(self, desc):
        """
        Set the description of the character.

        :param str desc: description
        """
        self.desc = desc

    def setImportant(self, important):
        """
        Set if the character is important/requires additional media.

        :param bool important: should the character be flagged as important
        """
        self.important = important


class Persona():
    """
    Class representing a Persona and it's stats.
    Spoilers, Shadows are also Personas.

    :param str arcana: the Persona's arcana
    :param str name: the Persona's name
    :param int level: starting level of this Persona (1-99)
    :param str desc: a short lore description of this Persona
    :param list[str] spellDeck: list of spells this Persona starts with
    :param dict spellLearn: spells learned and the level at which it is learned: {spellName: level}
    :param list[int] stats: Persona's stats at base level [Strength, Magic, Endurance, Agility, Luck]
    :param list[str] resistance: This Persona's elemental resistances (in P3 order)
    :param tuple heritage: prevelant elements for fusion algorithm
    :param str evolveName: the name of the Persona this one evolves into, if applicable
    """
    def __init__(self, name, arcana, level, desc, spellDeck, spellLearn,
                 stats, resistance, heritage, evolveName=None):
        self.name = name
        self.arcana = arcana
        self.level = level
        self.desc = desc
        self.spellDeck = spellDeck
        self.spellLearn = spellLearn
        self.stats = stats
        self.resistance = resistance
        self.heritage = heritage
        self.evolveName = evolveName

    def getArcana(self):
        """
        Get Persona's arcana.

        :returns: arcana
        :rtype: str
        """
        return self.arcana

    def getName(self):
        """
        Get Persona's name.

        :returns: name
        :rtype: str
        """
        return self.name

    def getEvolveName(self):
        """
        Get Persona's evolution, if applicable.

        :returns: name of evolved Persona, or None if no evolution
        :rtype: str|None
        """
        return self.evolveName

    def getLevel(self):
        """
        Get Persona's level.

        :returns: level
        :rtype: int
        """
        return self.level

    def getDesc(self):
        """
        Get Persona's description.

        :returns: description
        :rtype: str
        """
        return self.desc

    def getSpellDeck(self):
        """
        Get Persona's initial known spells.

        :returns: initial known spells
        :rtype: list[str]
        """
        return self.spellDeck

    def getSpellLearn(self):
        """
        Get Persona's learned spells and the levels at which they are learned.
        {spellName: level}

        :returns: spells learned
        :rtype: dict
        """
        return self.spellLearn

    def getStats(self):
        """
        Get Persona's starting stats.

        :returns: starting stats
        :rtype: list
        """
        return self.stats

    def getResistance(self):
        """
        Get Persona's elemental resistances.

        :returns: elemental resistances
        :rtype: list
        """
        return self.resistance

    def getHeritage(self):
        """
        Get Persona's preferred fusion spell inheritance type.

        :returns: one or two preferred elements
        :rtype: tuple
        """
        return self.heritage

    def setArcana(self, arcana):
        """
        Set Persona's arcana.

        :param str arcana: arcana
        """
        self.arcana = arcana

    def setName(self, name):
        """
        Set Persona's name.

        :param str name: name
        """
        self.name = name

    def setEvolveName(self, evolveName):
        """
        Set Persona's evolution, if desired.

        :param str evolveName: name of persona's evolution
        """
        self.evolveName = evolveName

    def setLevel(self, level):
        """
        Set Persona's starting level.

        :param int level: level
        """
        self.level = level

    def setDesc(self, desc):
        """
        Set Persona's description.

        :param str desc: description
        """
        self.desc = desc

    def setSpellDeck(self, spellDeck):
        """
        Set Persona's initial spell deck.

        :param list[str] spellDeck: initial spell deck
        """
        self.spellDeck = spellDeck

    def setSpellLearn(self, spellLearn):
        """
        Set all of Persona's learned spells.

        :param dict spellLearn: Spells learned and their levels
        """
        self.spellLearn = spellLearn

    def setStats(self, stats):
        """
        Set Persona's starting stats.

        :param list stats: [Strength, Magic, Endurance, Agility, Luck]
        """
        self.stats = stats

    def setResistance(self, resistance):
        """
        Set Persona's elemental resitances.

        :param list[str] resistance: List of elemental resistances in P3 order
        """
        self.resistance = resistance

    def setHeritage(self, heritage):
        """
        Set Persona's preferred fusion spell inheritance types.

        :param typle heritage: preferred spell elements to inherit (can be None)
        """
        self.heritage = heritage

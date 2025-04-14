# -*- coding: utf-8 -*-

from PyCharacterAI.types import CharacterShort,Character

class PcharacterMedium(CharacterShort):
    """CharacterShort but with slightly more data. Useful for checking if a bot has a privated definition"""
    def __init__(self, options):
        super().__init__(options)
        self.HasDefinition = options.get("has_definition",False)
    def isDefinitionPrivate(self):
        """Checks if the HasDefinition is True and if the definition field is empty"""
        if self.HasDefinition and self.definition == "":
            return True
        else:
            return False
    def isDefinitionPublic(self):
        """Checks if the HasDefinition is True and if the definition field is not empty"""
        return not self.isDefinitionPrivate()

class Pcharacter(Character):
    """Character but with slightly more data. Useful for checking if a bot has a privated definition"""
    def __init__(self, options):
        super().__init__(options)
        self.HasDefinition = options.get("has_definition",False)
    def isDefinitionPrivate(self):
        """Checks if the HasDefinition is True and if the definition field is empty"""
        if self.HasDefinition and self.definition == "":
            return True
        else:
            return False
    def isDefinitionPublic(self):
        """Checks if the HasDefinition is True and if the definition field is not empty"""
        return not self.isDefinitionPrivate()
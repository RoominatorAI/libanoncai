# -*- coding: utf-8 -*-

from enum import Enum, StrEnum
import requests
class SubscriptionType(StrEnum):
    Free = "NONE"
    Premium = "PLUS"

class PcharacterMedium():
    """CharacterShort but with slightly more data. Useful for checking if a bot has a privated definition"""
    def __init__(self, options):
        self.character_id = options.get("external_id")
        self.title = options.get("title", "")
        self.name = options.get("participant__name", None) 
        self.HasDefinition = options.get("has_definition",False)
        self.greeting = options.get("greeting", "")
        self.description = options.get("description", "")
        self.definition = options.get("definition", "")
    def isDefinitionPrivate(self):
        """Checks if the HasDefinition is True and if the definition field is empty"""
        if self.HasDefinition and self.definition == "":
            return True
        else:
            return False
    def isDefinitionPublic(self):
        """Checks if the HasDefinition is True and if the definition field is not empty"""
        return not self.isDefinitionPrivate()

class Pcharacter():
    """Character but with slightly more data. Useful for checking if a bot has a privated definition"""
    def __init__(self, options):
        self.character_id = options.get("external_id")
        self.title = options.get("title", "")
        self.name = options.get("participant__name", None) 
        self.HasDefinition = options.get("has_definition",False)
        self.greeting = options.get("greeting", "")
        self.description = options.get("description", "")
        self.definition = options.get("definition", "")
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
    

class AnonUser:
    """An anonymous user. Basically just metadata and what chars they own."""

    def __init__(self,object):
        self.chars = []
        for char in object.get("characters",[]):
            self.chars.append(PcharacterShort(char)) # Pcharacter requires data that isnt available from object so we just use normal character here.
        self.username = object.get("username")
        self.description = object.get("bio")
        self.subscription = SubscriptionType(object.get("subscription_type","NONE"))
        self.followers = object.get("num_followers",0)
        self.following = object.get("num_following",0)
        self.avatarURL = "https://characterai.io/i/400/static/avatars/" + object.get("avatar_file_name","")

    def getCharIDs(self):
        ids = []
        for char in self.chars:
            ids.append(char.character_id)
        return ids
    
    def doesExist(self): # checks if the user exists or is just a placeholder
        return not (self.username == None)
    
    def downloadAvatar(self,path="./avatar.png"): # downloads avatar to specified
        # NOTE the stream=True parameter below
        with requests.get(self.avatarURL, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)

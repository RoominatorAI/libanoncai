# -*- coding: utf-8 -*-
import requests
import json
from urllib.parse import quote
from .types import PcharacterMedium,Pcharacter, AnonUser
import aiohttp
import re
# Copilot tried to import aiohttp 4 TIMES. i am not even kidding. I had to remove the extra imports.
def get_latest_build_id(): # Makes sure that next.js calls actually work
    homepage = requests.get("https://character.ai")
    match = re.search(r'"buildId":"(.*?)"', homepage.text)
    if match:
        return match.group(1)
    return None
class Client():

    def __init__(self):
        """Initialize the libanoncai client. This is a wrapper around the PyCharacterAI client, but with anonymous support and extra functions."""
        self.anoncaiheaders = {
            "Content-Type": "application/json",
            "Referer": "https://character.ai/",
            "User-Agent": "Mozilla/5.0"
        } # Known working headers. May be seen as a bot, but whatever. We will rock you!


    def setUA(self,ua):
        """Set the User-Agent for the requests. This is useful for debugging and testing."""
        self.anoncaiheaders["User-Agent"] = ua

    def get_anonymous_search(self,searchQuery):
        # This is a dumb reverse-engineered function. Do not judge.

        payload = {
            "0": {
                "json": {
                    "searchQuery": searchQuery,
                    "tagId": None,
                    "sortedBy": None
                },
                "meta": {
                    "values": {
                        "tagId": ["undefined"],
                        "sortedBy": ["undefined"]
                    }
                }
            }
        }

        encoded_payload = quote(json.dumps(payload))
        url = f"https://character.ai/api/trpc/search.search?batch=1&input={encoded_payload}"

        try:
            res = requests.get(url, headers=self.anoncaiheaders)
            res.raise_for_status()
            data = res.json()
            chars = data[0]["result"]["data"]["json"].get("characters", [])
            return [PcharacterMedium(c) for c in chars]
        except Exception as e:
            print(f"💀 Search API exploded: {e}")
            return [] # We should honestly return an error in-ui but eh, it'll be fine for now.

    def get_anonymous_featured(self, category="Entertainment & Gaming"):
        # This is a shitty API that is not even documented. We just reverse engineered it.
        # It is used by the website. I just used devtools and yanked the API from there.

        payload = {
            "0": {
                "json": {
                    "category": category
                }
            }
        }

        url = "https://character.ai/api/trpc/discovery.charactersByCuratedAnon?batch=1&input=" + requests.utils.quote(json.dumps(payload))
        # Reverse engineered, but not using PyCharacterAI as it threw a hissy fit when anonymous.
        res = requests.get(url, headers=self.anoncaiheaders)
        data = res.json()
        chars = data[0]["result"]["data"]["json"].get("characters", [])
        cshorts = []
        for char in chars:
            cshorts.append(PcharacterMedium(char))
        return cshorts # Converting back to CharacterShort subclass so we can use them in the same way as PyCharacterAI does, except we use a different API endpoint.

    def get_anonymous_chardef(self,character_id):
        payload = {
            "0": {
                "json": {
                    "externalId": character_id
                }
            }
        }

        url = "https://character.ai/api/trpc/character.info?batch=1&input=" + requests.utils.quote(json.dumps(payload))
        # Reverse engineered, but not using PyCharacterAI as it threw a hissy fit when anonymous.
        res = requests.get(url, headers=self.anoncaiheaders)
        data = res.json()
        print(data)
        res = data[0]["result"]["data"]["json"]
        if res["status"] == "OK":
            return PcharacterMedium(res["character"]) # We convert this to a CharacterShort so we can use it in the same way as PyCharacterAI does, except we use a different API endpoint.
        else:
            print(f"💀 Get API be angy! {res['error']}")
            return None # We should honestly return an error in-ui but eh, it'll be fine for now.

    def get_anonymous_user(self,username):

        url = f"https://character.ai/_next/data/{get_latest_build_id()}/profile/{username}.json?username={username}" # Somehow this URL works. I don't know
        # Nextjs is just black magic to me.
        cheaders = self.anoncaiheaders.copy()
        cheaders["x-nextjs-data"] = "1" # Makes sure next doesnt spam us with html. We only need the json data.
        res = requests.get(url,headers=cheaders)

        if res.status_code == 200:
            data = res.json().get("pageProps",{}).get("dehydratedState",{}).get("queries",[])[0].get("state",{}).get("data",{})
            # holy shit thats a lot of get calls. I don't know how this works.
            return AnonUser(data)


    def multiget_anonymous_chardef(self,character_ids):
        amount = len(character_ids)
        payload = {
        }
        for index,charid in enumerate(character_ids):
            payload[str(index)] = {
                "json": {
                    "externalId": charid
                }
            }
        commands = ""
        for index in range(amount):
            commands += "character.info"
            if index != amount - 1:
                commands += ","
        url = f"https://character.ai/api/trpc/{commands}?batch={amount}&input=" + requests.utils.quote(json.dumps(payload))
        res = requests.get(url, headers=self.anoncaiheaders)
        data = res.json()
        out = []
        for result in data:
            res = result["result"]["data"]["json"]
            if res["status"] == "OK":
                out.append(PcharacterMedium(res["character"]))
            else:
                print(f"💀 Multiget API be angy! {res['error']}")
        return out

    def convertCharacterShortToPcharacterMedium(self,character):
        """Converts a CharacterShort to a PcharacterMedium. This is useful for when you want to use the PcharacterMedium class but you have a CharacterShort."""
        return self.get_anonymous_chardef(character.character_id)
    def multiConvertCharacterShortToPcharacterMedium(self,characters):
        """Converts a list of CharacterShorts to a list of PcharacterMediums. This is useful for when you want to use the PcharacterMedium class but you have a list of CharacterShorts."""
        ids = []
        for character in characters:
            ids.append(character.character_id)
        return self.multiget_anonymous_chardef(ids)

r"""
 _     _ _                                       _ 
| |   (_) |                                     (_)
| |    _| |__   __ _ _ __   ___  _ __   ___ __ _ _ 
| |   | | '_ \ / _` | '_ \ / _ \| '_ \ / __/ _` | |
| |___| | |_) | (_| | | | | (_) | | | | (_| (_| | |
\_____/_|_.__/ \__,_|_| |_|\___/|_| |_|\___\__,_|_|
                                                   
# Libanoncai: Extending PyCharacterAI with anonymous support. Powered by tRPC sniffing.                                                   
"""


# Async Client

class AsyncClient(Client):
    def __init__(self):
        """Initialize the async libanoncai client."""
        super().__init__()

    async def get_anonymous_search(self, searchQuery):
        payload = {
            "0": {
                "json": {
                    "searchQuery": searchQuery,
                    "tagId": None,
                    "sortedBy": None
                },
                "meta": {
                    "values": {
                        "tagId": ["undefined"],
                        "sortedBy": ["undefined"]
                    }
                }
            }
        }
        encoded_payload = quote(json.dumps(payload))
        url = f"https://character.ai/api/trpc/search.search?batch=1&input={encoded_payload}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.anoncaiheaders) as response:
                data = await response.json()
                chars = data[0]["result"]["data"]["json"].get("characters", [])
                return [PcharacterMedium(c) for c in chars]

    async def get_anonymous_featured(self, category="Entertainment & Gaming"):
        payload = {
            "0": {
                "json": {
                    "category": category
                }
            }
        }
        url = "https://character.ai/api/trpc/discovery.charactersByCuratedAnon?batch=1&input=" + quote(json.dumps(payload))
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.anoncaiheaders) as response:
                data = await response.json()
                chars = data[0]["result"]["data"]["json"].get("characters", [])
                return [PcharacterMedium(c) for c in chars]

    async def get_anonymous_chardef(self, character_id):
        payload = {
            "0": {
                "json": {
                    "externalId": character_id
                }
            }
        }
        url = "https://character.ai/api/trpc/character.info?batch=1&input=" + quote(json.dumps(payload))
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.anoncaiheaders) as response:
                data = await response.json()
                res = data[0]["result"]["data"]["json"]
                return PcharacterMedium(res["character"]) if res["status"] == "OK" else None

    async def multiget_anonymous_chardef(self, character_ids):
        payload = {str(i): {"json": {"externalId": cid}} for i, cid in enumerate(character_ids)}
        commands = ",".join(["character.info"] * len(character_ids))
        url = f"https://character.ai/api/trpc/{commands}?batch={len(character_ids)}&input=" + quote(json.dumps(payload))
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.anoncaiheaders) as response:
                data = await response.json()
                return [PcharacterMedium(r["result"]["data"]["json"]["character"]) 
                        for r in data if r["result"]["data"]["json"]["status"] == "OK"]
    
    async def get_anonymous_user(self,username):
        url = f"https://character.ai/_next/data/{get_latest_build_id()}/profile/{username}.json?username={username}" # Somehow this URL works. I don't know
        # Nextjs is just black magic to me.
        cheaders = self.anoncaiheaders.copy()
        cheaders["x-nextjs-data"] = "1" # Makes sure next doesnt spam us with html. We only need the json data.
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=cheaders) as res:

                if res.status == 200:
                    decoded = await res.json()
                    data = decoded.get("pageProps",{}).get("dehydratedState",{}).get("queries",[])[0].get("state",{}).get("data",{})
                    # holy shit thats a lot of get calls. I don't know how this works.
                    return AnonUser(data)
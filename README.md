# Libanoncai
Libanoncai is an extension to PyCharacterAI, that adds a way for you to anonymously use their tRPC api.

> [!CAUTION]
> We are NOT responsible for any IP blocks caused by Libanoncai.

Libanoncai is NOT a monkeypatch, but has a very simple API anyways.

## Usage:

Example Code
```py
import libanoncai
client = libanoncai.Client()
bot = client.get_anonymous_search("Blank")[0] # Why not?
print(bot.name)
```
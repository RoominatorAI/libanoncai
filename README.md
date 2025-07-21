# Libanoncai
Libanoncai is an extension to PyCharacterAI, that adds a way for you to anonymously use their tRPC api.

> [!CAUTION]
> We are NOT responsible for any IP blocks caused by Libanoncai.

Libanoncai is NOT a monkeypatch, but has a very simple API anyways.

V1.2.0 fixes multiget with many characters at once by limiting multiget internally to 10 ids per request. This makes more requests internally but lets you request a lot more at once.

V1.2.1 fixed broken multiget and now v1.2.0 is yanked.

## Usage:

Example Code
```py
import libanoncai
client = libanoncai.Client()
bot = client.get_anonymous_search("Blank")[0] # Why not?
print(bot.name)
```
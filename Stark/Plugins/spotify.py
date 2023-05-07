import os 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from Stark import error_handler
from Stark.config import Config
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

SPT_CLIENT = Config.SPT_CLIENT
SPT_SECRET = Config.SPT_SECRET

client_credentials_manager = SpotifyClientCredentials(client_id=SPT_CLIENT, client_secret=SPT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@Client.on_message(filters.command(["spotify"]))
@error_handler
async def spotify_search(c, m):
  try:
    query = m.text.split(None, 1)[1]
  except IndexError:
    await m.reply_text("`Gib some input to search..`")
    return
  spt = await m.reply_text("`Searching for your song...`")
  results = sp.search(q=query, type='track')
  m = f"**Sᴇᴀʀᴄʜ Qᴜᴇʀʏ:** `{query}`\n**Rᴇꜱᴜʟᴛꜱ: \n\n‎ "
  for track in results['tracks']['items']:
      lnk = track['external_urls']['spotify']
      name = f"{track['name']} - {track['artists'][0]['name']}"
      msg = f"‎‎  ➣ __**[{name} 🎧]({lnk})**__\n"
      m = m+msg 
  await spt.edit(m, disable_web_page_preview=True, parse_mode = ParseMode.MARKDOWN)
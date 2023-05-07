import os 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from Stark import error_handler
from pyrogram import Client, filters

client_credentials_manager = SpotifyClientCredentials(client_id='e5f24fc4807b4bb6afa62e92fb607875', client_secret='08a5ff44ba7d47e4867983392b5a7ef0')
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
  m = f"**Sᴇᴀʀᴄʜ Qᴜᴇʀʏ:** `{query}`\n**Rᴇꜱᴜᴋᴛꜱ: \n"
  for track in results['tracks']['items']:
      lnk = track['external_urls']['spotify']
      name = f"{track['name']} - {track['artists'][0]['name']}"
      msg = f"‎ ➣ [{name} 🎧]({lnk})\n"
      m = m+msg 
  await spt.edit(m, disable_web_page_preview=True)
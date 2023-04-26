import os
import base64
from urllib.parse import quote
from pyrogram import Client, filters


async def carbon(code):
   url = f"https://api.safone.me/carbon?code={quote(code)}"
   return url

@Client.on_message(filters.command(["carbon"]))
async def make_carbon(bot, message):    
    ok = await message.reply_text("`Making Carbon...`") 
    code = None
    if message.reply_to_message:
          if message.reply_to_message.caption:
               code = message.reply_to_message
          elif message.reply_to_message.text:
              code = message.reply_to_message.text
    elif len(message.command) > 1:
        code = message.text.split(" ",1)[1]
        
    if not code:
           return await ok.edit("`Nothing To Carbonize...`")
           
    x = await carbon(code)
    carbon_url = x["image"]
    decodeit = open('carbon.jpg', 'wb')
    decodeit.write(base64.b64decode((carbon_url)))
    decodeit.close()
    if message.from_user:
        user = message.from_user.mention
    else:
        user = message.sender_chat.title
    cap = f"__Carbonized By {user}__\n\n__**By @Mr_StatkBot**"
    await message.reply_document("carbon.jpg", caption=cap)
    await ok.delete()


@Client.on_message(filters.command(["icarbon"]))
async def carbonn(bot, message):    
    ok = await message.reply_text("Making Carbon...") 
    code = None
    if message.reply_to_message:
          if message.reply_to_message.caption:
               code = message.reply_to_message
          elif message.reply_to_message.text:
              code = message.reply_to_message.text
    elif len(message.command) > 1:
        code = message.text.split(" ",1)[1]
                  
    if not code:
           return await ok.edit("Nothing To Carbonize...")
           
    x = await carbon(code)
    carbon_url = x["image"]
    decodeit = open('carbon.jpg', 'wb')
    decodeit.write(base64.b64decode((carbon_url)))
    decodeit.close()
    if message.from_user:
        user = message.from_user.mention
    else:
        user = message.sender_chat.title
    cap = f"__Carbonized By {user}__\n\n__**By @Mr_StatkBot**"
    await bot.send_photo(message.chat.id, "carbon.jog", caption=cap)
    await ok.delete()
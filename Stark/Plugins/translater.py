from pyrogram import Client, filters
from pyrogram.types import Message
from SafoneAPI import SafoneAPI
from Stark import error_handler

api = SafoneAPI()

@Client.on_message(filters.command(["tr", "translate"]))
@error_handler
async def translate_me(client: Client, message: Message):
    lang = message.text.split(None, 1)
    target_lang = lang[1] if len(lang) > 1 else "en"
    
    reply_message = message.reply_to_message
    if not reply_message or not reply_message.text:
        await message.reply_text("`Reply to a message containing text to translate it`")
        return
    
    text = reply_message.text
    translated = await api.translate(text, target=target_lang)
    result = translated.translated

    await message.reply_text(f"**➥Translated successfully:**\n\n➥`{result}`")

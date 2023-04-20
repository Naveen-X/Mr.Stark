import os
import openai
import requests 
from pyrogram import Client, filters

openai.api_key = "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"

def generate_response(user_input):
    prompt = user_input
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message

@Client.on_message(filters.command(['gpt', 'askgpt', 'chatgpt']))
async def chatbot(bot, message):
    try:
      query = message.text.split(None, 1)[1]
    except:
        await message.reply_text(
            "`ɪ ᴅɪᴅɴ'ᴛ ɢᴇᴛ ᴛʜᴀᴛ`"
        )
        return
    response = generate_response(query)
    await bot.send_message(message.chat.id, response, reply_to_message_id=message.id)
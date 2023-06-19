import os

import pyqrcode
from pyrogram import Client, filters

from Stark import error_handler


@Client.on_message(filters.command('qr'))
@error_handler
async def qr(c, m):
    global qr_code
    if " " in m.text:
        tdl = await m.reply('Plz Wait brouh!')
        text = str(m.text).split(" ", 1)[1]
        img = pyqrcode.create(text)
        kmg = img.png('qr.png', scale=40)
        # print(kmg)#img.save('qr.png')
        try:
            await c.send_photo(m.chat.id, 'qr.png')
        except:
            await c.send_document(m.chat.id, 'qr.png')
        await tdl.delete()
    elif not m.reply_to_message:
        await m.reply(
            'hah! what to do with empty command?\nReply an image to scan or send text along with command to make qr.')
    elif m.reply_to_message.photo:
        x = await m.reply_text("`Processing...`")
        try:
            import cv2
            d = cv2.QRCodeDetector()
            qr_code = await m.reply_to_message.download()
            val, p, s = d.detectAndDecode(cv2.imread(qr_code))
            await x.edit(val)
        except:
            await x.edit("`Failed to get data`")
        os.remove(qr_code)
    else:
        await m.reply('`Unsupported!`')

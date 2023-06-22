import os
import cv2
import qrcode
from pyrogram import Client, filters
from Stark import error_handler

@Client.on_message(filters.command('qr'))
@error_handler
async def qr(c, m):
    if " " in m.text:
        tdl = await m.reply_text("**Plz wi8 Bruh!!**")
        text = str(m.text).split(" ", 1)[1]
        qr = qrcode.QRCode(version=None,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr.png')
        try:
            await c.send_photo(m.chat.id, 'qr.png')
        except:
            await c.send_document(m.chat.id, 'qr.png')
        os.remove('qr.png')
    elif m.reply_to_message.text:
        text = m.reply_to_message.text
        qr = qrcode.QRCode(version=None,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qr.png')
        try:
            await c.send_photo(m.chat.id, 'qr.png')
        except:
            await c.send_document(m.chat.id, 'qr.png')
        os.remove('qr.png')
    elif not m.reply_to_message:
        await m.reply(
            '**Hah! What to do with empty command?\nReply an image to scan or send text along with command to make qr.**')
    elif m.reply_to_message.photo:
        x = await m.reply_text("Processing...")
        try:
            d = cv2.QRCodeDetector()
            qr_code = await m.reply_to_message.download()
            val, p, s = d.detectAndDecode(cv2.imread(qr_code))
            await x.edit(val)
        except:
            await x.edit("Failed to get data")
        os.remove(qr_code)
    else:
        await m.reply('Unsupported!')
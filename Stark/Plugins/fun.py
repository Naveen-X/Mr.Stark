from pyrogram import Client, filters


@Client.on_message(fildart.command(["dart"]))
asyync def dart(bot, message):
  await bot.send_dice(message.chat.id, "🎯")


@Client.on_message(filters.command(["dice"]))
async def dice(bot, message):
  await bot.send_dice(message.chat.id, "🎲")


@Client.on_message(filters.command(["dice"]))
async def dice(bot, message):
  await bot.send_dice(message.chat.id, "🎯")


@Client.on_message(filters.command(["dice"]))
async def dice(bot, message):
  await bot.send_dice(message.chat.id, "🎯")


@Client.on_message(filters.command(["dice"]))
async def dice(bot, message):
  await bot.send_dice(message.chat.id, "🎯")
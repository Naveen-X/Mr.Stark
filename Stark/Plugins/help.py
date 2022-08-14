from Script import script
from pyrogram import Client, filters
from pyromod.nav import Pagination
from pyromod.helpers import ikb
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def page_data(page):
    return f'help_{page}'
def item_data(item,page):
    return f'help_{item}'
def item_title(item,page):
    return f'{item}'

@Client.on_message(filters.command(['help','hlp','h']))
async def hi(c,m):
  objects = [ x for x in dir(script) if not x.startswith('__')]
  page = Pagination(
        objects,
        page_data=page_data,
        item_data=item_data, 
        item_title=item_title
    )
  index = 0
  lines = 4 
  columns =3
  kb = page.create(index, lines, columns)
  await m.reply('Help Menu of Stark!', reply_markup=ikb(kb))


@Client.on_callback_query()
async def cbdta(client,query):
  q = query
  #print(q.data)
  if "close" in q.data:
    await q.answer('delete if you can! i cant.', alert=True)
  elif "help_" in q.data:
    hlp = q.data.split('help_')[1]
    #print(hlp)
    await q.edit_message_text(text = (getattr(script, hlp)),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Back', callback_data='hlp'), InlineKeyboardButton(text='Home', callback_data='back')],[InlineKeyboardButton(text='System Stats', callback_data='sys_info'), InlineKeyboardButton(text='About me', callback_data='about')],[InlineKeyboardButton(text='Close', callback_data='close'),] ]))
  elif "hlp" in q.data:
    objects = [ x for x in dir(script) if not x.startswith('__')]
    page = Pagination(
        objects,
        page_data=page_data,
        item_data=item_data, 
        item_title=item_title
    )
    index = 0
    lines = 4 
    columns =3
    kb = page.create(index, lines, columns)
    await q.message.edit('Help Menu of Stark!', reply_markup=ikb(kb))
    
  

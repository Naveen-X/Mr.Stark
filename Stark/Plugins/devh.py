import requests
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from Stark import error_handler, db

# Store user DevH mappings in MongoDB
async def add_devh_user(user_id: int, devh_user_id: str):
    """Add user to DevH database mapping"""
    global db
    collection = db.DB.devh_users
    
    # Check if user already exists
    existing = collection.find_one({'telegram_id': user_id})
    if existing:
        # Update existing record
        collection.update_one(
            {'telegram_id': user_id},
            {'$set': {'devh_user_id': devh_user_id}}
        )
    else:
        # Insert new record
        collection.insert_one({
            'telegram_id': user_id,
            'devh_user_id': devh_user_id
        })

async def get_devh_user(user_id: int):
    """Get DevH user ID for telegram user"""
    global db
    collection = db.DB.devh_users
    user_data = collection.find_one({'telegram_id': user_id})
    return user_data['devh_user_id'] if user_data else None

@Client.on_message(filters.command("devh"))
@error_handler
async def devh_add_user(client: Client, message: Message):
    """Add user to DevH database with /devh {user_id}"""
    
    # Check if user provided user_id
    if len(message.command) < 2:
        await message.reply_text("**Usage:** `/devh {user_id}`\n\nPlease provide your DevH user ID.")
        return
    
    devh_user_id = message.command[1]
    telegram_user_id = message.from_user.id
    
    try:
        # Add to database
        await add_devh_user(telegram_user_id, devh_user_id)
        await message.reply_text(f"✅ **DevH User Added Successfully!**\n\n**Telegram ID:** `{telegram_user_id}`\n**DevH User ID:** `{devh_user_id}`\n\nYou can now use `/now` command to get your Spotify now playing image!")
        
    except Exception as e:
        await message.reply_text(f"❌ **Error adding DevH user:**\n`{e}`")




@Client.on_message(filters.command("now"))
@error_handler
async def devh_now_playing(client: Client, message: Message):
    """Get Spotify now playing image from DevH API"""
    
    telegram_user_id = message.from_user.id
    
    # Get DevH user ID from database
    devh_user_id = await get_devh_user(telegram_user_id)
    
    if not devh_user_id:
        await message.reply_text("❌ **DevH user not found!**\n\nPlease first add your DevH user ID using:\n`/devh {your_user_id}`")
        return
    
    # Send "fetching" message
    status_msg = await message.reply_text("🎵 **Fetching your Spotify now playing...**")
    
    try:
        # Call DevH API
        api_url = f"https://devh.in/api/users/{devh_user_id}/spotify/now-playing.png"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    # Success - download and send image
                    image_data = await response.read()
                    
                    # Save temporarily
                    temp_filename = f"now_playing_{telegram_user_id}.png"
                    with open(temp_filename, 'wb') as f:
                        f.write(image_data)
                    
                    # Send image
                    await client.send_photo(
                        chat_id=message.chat.id,
                        photo=temp_filename,
                        caption=f"🎵 **Now Playing - {message.from_user.first_name}**\n\n*Powered by DevH*",
                        reply_to_message_id=message.id
                    )
                    
                    # Clean up
                    import os
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)
                    
                    await status_msg.delete()
                    
                else:
                    # API error
                    error_text = await response.text()
                    await status_msg.edit(f"❌ **DevH API Error:**\n\n**Status Code:** `{response.status}`\n**Response:** `{error_text}`\n\n*Make sure your DevH user ID is correct and you're currently playing music on Spotify.*")
                    
    except Exception as e:
        await status_msg.edit(f"❌ **Error fetching now playing:**\n`{e}`")

@Client.on_message(filters.command("devh_info"))
@error_handler
async def devh_user_info(client: Client, message: Message):
    """Show current DevH user info"""
    
    telegram_user_id = message.from_user.id
    devh_user_id = await get_devh_user(telegram_user_id)
    
    if devh_user_id:
        await message.reply_text(f"ℹ️ **Your DevH Info:**\n\n**Telegram ID:** `{telegram_user_id}`\n**DevH User ID:** `{devh_user_id}`\n\n**Available Commands:**\n• `/now` - Get Spotify now playing image\n• `/devh [user_id]` - Update DevH user ID")
    else:
        await message.reply_text("❌ **No DevH user found!**\n\nUse `/devh [user_id]` to add your DevH user ID first.")

from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Stark import error_handler

ia = IMDb()

@Client.on_message(filters.command(["imdb"]))
@error_handler
async def search_movie(bot, message):
    if len(message.command) < 2:
        await bot.send_message(
            chat_id=message.chat.id,
            text="`Please provide a movie or TV series name after the /imdb command.`"
        )
        return

    query = " ".join(message.command[1:])
    movies = ia.search_movie(query)
    if movies:
        movie = movies[0]
        ia.update(movie, ['main', 'plot', 'genres', 'runtime', 'rating', 'director', 'cast', 'cover url', 'streaming sites'])
        title = movie.get('title')
        year = movie.get('year')
        rating = movie.get('rating')
        plot = movie.get('plot')
        genres = ', '.join(movie.get('genres', []))
        runtime = movie.get('runtime')
        director = movie.get('director')
        cast = ', '.join([actor['name'] for actor in movie.get('cast', [])[:5]])
        cover_url = movie.get('cover url')
        streaming_sites = movie.get('streaming sites', [])

        message_text = f"🎬 **{title}**\n\n"
        message_text += f"📅 Year: `{year}`\n"
        message_text += f"⭐️ Rating: `{rating}`\n"
        message_text += f"🎭 Genres: `{genres}`\n"
        message_text += f"⏱️ Runtime: `{runtime} minutes`\n"
        message_text += f"🌟 Cast: `{cast}`\n\n"
        message_text += f"📝 Plot: `{plot}`\n"

        if streaming_sites:
            sites_text = "**__Available Streaming Sites:__**\n"
            for site in streaming_sites:
                sites_text += f"• `{site}`\n"
            message_text += f"\n`{sites_text}`"

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("IMDb Page", url=f"https://www.imdb.com/title/{movie.movieID}/")],
                [InlineKeyboardButton("More Details", callback_data=f"more_details_{movie.movieID}")]
            ]
        )

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=cover_url,
            caption=message_text,
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="No movie or TV series found with that name."
        )
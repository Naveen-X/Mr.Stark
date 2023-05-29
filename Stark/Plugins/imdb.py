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
        ia.update(movie, ["main", "plot", "cast", "cover url", "language", "countries", "plot outline"])

        title = movie["title"]
        year = movie["year"]
        rating = movie["rating"]
        plot = movie["plot"][0]
        genres = ", ".join(movie["genres"])
        cast = ", ".join([actor["name"] for actor in movie["cast"][:5]])
        runtime = movie["runtimes"][0]
        lang = movie["language"][0]
        cover_url = movie.get("cover url", "")

        message_text = f"🎬 **{title}**\n\n"
        message_text += f"📅 Year: `{year}`\n"
        message_text += f"⭐️ Rating: `{rating}`\n"
        message_text += f"🎭 Genres: `{genres}`\n"
        message_text += f"🌐 Language: `{lang}`\n"
        message_text += f"⏱️ Runtime: `{runtime} minutes`\n"
        message_text += f"🌟 Cast: `{cast}`\n\n"
        message_text += f"📝 Plot: __{plot}__"

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
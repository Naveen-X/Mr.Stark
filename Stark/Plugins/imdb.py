import os 
try:
	from imdb import IMDb 
except:
	os.system("pip install imdb")
	from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Stark import error_handler

ia = IMDb()

@Client.on_message(filters.command(["imdb", "IMDb"]))
@error_handler
async def search_movie(bot, message):
    if len(message.command) < 2:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Please provide a movie or TV series name after the /imdb command."
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
        director = movie["director"][0]["name"]
        cast = ", ".join([actor["name"] for actor in movie["cast"][:5]])
        runtime = movie["runtimes"][0]
        language = movie["language"][0]
        countries = ", ".join(movie["countries"])
        plot_outline = movie.get("plot outline", "")
        cover_url = movie.get("cover url", "")

        caption = f"🎬 Title: {title}\n"
        caption += f"⭐️ Rating: {rating}\n"
        caption += f"🔍 Plot: {plot}\n"
        caption += f"📅 Year: {year}\n"
        caption += f"🌟 Genres: {genres}\n"
        caption += f"🎬 Director: {director}\n"
        caption += f"🌐 Language: {language}\n"
        caption += f"🌍 Countries: {countries}\n"
        caption += f"⏱️ Runtime: {runtime} mins\n"

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=cover_url,
            caption=caption,
            reply_markup=get_inline_keyboard(movie.movieID)
        )
    else:
        await message.reply_text("No movie found.")

# Define the callback query handler
@Client.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if data.startswith("streaming_sites_"):
        movie_id = data.split("_")[2]
        
        # Fetch streaming sites for the movie using IMDbPY or any other method
        movie = ia.get_movie(movie_id)
        streaming_sites = movie.get('streaming_sites')
        
        if streaming_sites:
            keyboard = []
            for site in streaming_sites:
                button = InlineKeyboardButton(text=site, url=streaming_sites[site])
                keyboard.append([button])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            message_text = "Click on the streaming site:"
        else:
            reply_markup = None
            message_text = "No streaming sites available for this movie."
        
        await callback_query.answer()
        await callback_query.message.edit_text(
            text=message_text,
            reply_markup=reply_markup
        )

def get_inline_keyboard(movie):
    keyboard = []
    streaming_sites_button = InlineKeyboardButton(
        text="Streaming Sites",
        callback_data=f"streaming_sites_{movie}"
    )
    keyboard.append([streaming_sites_button])
    return InlineKeyboardMarkup(keyboard)
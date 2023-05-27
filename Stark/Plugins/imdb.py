import os
import requests 
from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Stark import error_handler

ia = IMDb()

@Client.on_message(filters.command(["imdb", "IMDb"]))
@error_handler
async def search_movie(bot, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a movie or TV series name after the /imdb command.")
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

        poster_path = f"poster_{movie.movieID}.jpg"
        response = requests.get(cover_url)
        with open(poster_path, "wb") as file:
            file.write(response.content)

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=poster_path,
            caption=caption,
            reply_markup=get_inline_keyboard(movie.movieID)
        )
        os.remove(poster_path)
    else:
        await message.reply_text("No movie found.")

def generate_movie_caption(movie):
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

    return generate_movie_caption
    
# Define the callback query handler
@Client.on_callback_query()
async def callback_handler(bot, callback_query):
    data = callback_query.data
    if data == "back":
        movie_id = callback_query.message.reply_markup.inline_keyboard[0][0].callback_data
        movie = ia.get_movie(movie_id)
        caption = generate_movie_caption(movie)
        reply_markup = get_inline_keyboard(movie_id)

        await callback_query.message.edit_text(
            text=caption,
            reply_markup=reply_markup
        )

    elif data.startswith("streaming_sites_"):
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
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="back")]])
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

@Client.on_message(filters.command(["test"]))
@error_handler
async def search_movie(bot, message):
    if len(message.command) < 2:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Please provide a movie or TV series name after the /imdb command."
        )
        return

    query = " ".join(message.command[1:])
    # Perform a search query to obtain the movie details
    response = requests.get(f"https://apis.justwatch.com/content/titles/en_US/popular?query={query}")
    data = response.json()

    if data.get("items"):
        movie = data["items"][0]

        title = movie["title"]
        year = movie["original_release_year"]
        rating = movie["scoring"]["imdb"]
        plot = movie["short_description"]
        genres = ", ".join(movie["genre_ids"])
        streaming_sites = get_streaming_sites(movie)
        
        caption = f"🎬 Title: {title}\n"
        caption += f"⭐️ Rating: {rating}\n"
        caption += f"🔍 Plot: {plot}\n"
        caption += f"📅 Year: {year}\n"
        caption += f"🌟 Genres: {genres}\n"
        caption += f"🌐 Streaming Sites: {', '.join(streaming_sites)}\n"

        await bot.send_message(
            chat_id=message.chat.id,
            text=caption,
            reply_markup=get_inline_keyboard(streaming_sites)
        )
    else:
        await message.reply_text("No movie found.")

def get_streaming_sites(movie):
    # Extract streaming site information from the movie data
    offers = movie.get("offers", [])
    streaming_sites = []

    for offer in offers:
        if offer.get("monetization_type") == "flatrate":
            streaming_sites.append(offer["provider_id"])

    return streaming_sites

def get_inline_keyboard(streaming_sites):
    keyboard = []
    
    for site in streaming_sites:
        # Customize the button labels and URLs based on the streaming site
        if site == "netflix":
            button = InlineKeyboardButton(text="Netflix", url="https://www.netflix.com/")
        elif site == "amazon_prime":
            button = InlineKeyboardButton(text="Amazon Prime", url="https://www.amazon.com/primevideo")
        elif site == "hulu":
            button = InlineKeyboardButton(text="Hulu", url="https://www.hulu.com/")
        else:
            # Add more streaming site options as needed
            button = InlineKeyboardButton(text=site.capitalize(), url="https://example.com/")
        
        keyboard.append([button])

    return InlineKeyboardMarkup(keyboard)
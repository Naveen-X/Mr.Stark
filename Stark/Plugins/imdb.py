from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Stark import error_handler

ia = IMDb()
movie_name_db = {}

@Client.on_message(filters.command(["imdb", "IMDb"]))
@error_handler
async def search_movie(client, message):
    if len(message.command) < 2:
        await client.send_message(
            chat_id=message.chat.id,
            text="`Please provide a movie or TV series name after the /imdb command.`"
        )
        return
    # Get the movie name from the user's message 
    movie_name = message.text.split(" ", 1)[1]
    movie_name_db.update({"name": movie_name})
    mv = await message.reply_text(f"`Searching for {movie_name}`")

    # Search for the movie using IMDbPY
    movies = ia.search_movie(movie_name, results=10)

    # If no movies were found, send a message to the user and return
    if len(movies) == 0:
        await message.reply_text("**__No movies found with that name!__**")
        return

    # Create a list of buttons for each search result
    button_list = []
    for i, movie in enumerate(movies[:10]):
        button_list.append([InlineKeyboardButton(text=movie['title'], callback_data=f"select_movie {i}")])

    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup(button_list)

    # Send a message to the user with the search results and buttons
    message_text = f"Found {len(movies)} results. Please select a movie:"
    await mv.edit(
        text=message_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


# Define the callback query handler for selecting a movie
@Client.on_callback_query(filters.regex("^select_movie"))
async def select_movie_handler(client, callback_query):
    # Get the index of the selected movie from the callback callback_data
    await callback_query.answer("Hold on...", show_alert=True)
    index = int(callback_query.data.split(" ")[1])
    movie_name = get_movie_name = movie_name_db.get("name")
    # Search for the movie using IMDbPY
    movie_id = ia.search_movie(movie_name, results=10)[index].getID()
    movie = ia.get_movie(movie_id)

    # Get the URL of the movie poster, if available
    if 'full-size cover url' in movie.keys():
        poster_url = movie['full-size cover url']
    elif 'cover url' in movie.keys():
        poster_url = movie['cover url']
    else:
        poster_url = None

    # Create a message with the movie details and poster
    movie_msg = f"<b>🎬 {movie['title']}</b> ({movie['year']})\n\n"
    movie_msg += f"<b>⭐️ Rating:</b> {movie['rating']}\n"
    movie_msg += f"<b>🎭 Genres:</b> {' | '.join(movie['genres'])}\n\n"
    movie_msg += f"📝: {movie['plot'][0]}...\n"

    # Create inline keyboard with two buttons
    view_button = InlineKeyboardButton(text="View on IMDb", url=f"https://www.imdb.com/title/tt{movie.getID()}/")
    more_details_button = InlineKeyboardButton(text="More Details", callback_data=f"more_details {movie.getID()}")

    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup([[view_button], [more_details_button]])

    # Send the message with the poster and button_list 
    await callback_query.message.reply_photo(
        photo=poster_url,
        caption=movie_msg,
        reply_markup=keyboard,
    )
    await callback_query.message.delete()


# Define the callback query handler for the "More Details" button
@Client.on_callback_query(filters.regex("^more_details"))
async def more_details_handler(client, callback_query):
    # Get the IMDb ID of the movie from the callback data
    imdb_id = callback_query.data.split(" ")[1]
    await callback_query.answer("Ok")

    # Get the details of the movie using IMDbPY
    movie = ia.get_movie(imdb_id)

    # Create a message with the movie details
    movie_msg = f"<b>🎬 {movie['title']}</b> ({movie['year']})\n\n"
    movie_msg += f"<b>⭐️ Rating:</b> {movie['rating']}\n"
    movie_msg += f"<b>🎭 Genres:</b> {' | '.join(movie['genres'])}\n"
    movie_msg += f"<b>🌐 Language:</b> {' | '.join(movie['language'])}\n"
    movie_msg += f"<b>⏱️ Runtime:</b> {movie['runtimes'][0]} minutes\n"
    movie_msg += f"<b>📝 Plot:</b> {movie['plot'][0]}...\n"
    movie_msg += f"\n<b>🌟 Cast:</b>\n"

    # Add the cast members to the message
    for person in movie['cast'][:5]:
        movie_msg += f"- {person['name']} ({person.currentRole})\n"

    # Send the message with the movie Details	
    view_button = InlineKeyboardButton(text="View on IMDb", url=f"https://www.imdb.com/title/tt{movie.getID()}/")
    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup([[view_button]])
    await callback_query.message.edit_text(
        text=movie_msg,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )
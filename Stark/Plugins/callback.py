from imdb import IMDb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ia = IMDb()


# @Client.on_callback_query(filters.regex("^select_movie"))
# async def select_movie_handler(client, callback_query):
#     # Get the index of the selected movie from the callback callback_data
#     await callback_query.answer("Hold on...", show_alert=True)
#     index = int(callback_query.data.split(" ")[1])
#     movie_name = get_movie_name = movie_name_db.get("name")
#     # Search for the movie using IMDbPY
#     movie_id = ia.search_movie(movie_name, results=10)[index].getID()
#     movie = ia.get_movie(movie_id)
#
#     # Get the URL of the movie poster, if available
#     if 'full-size cover url' in movie.keys():
#         poster_url = movie['full-size cover url']
#     elif 'cover url' in movie.keys():
#         poster_url = movie['cover url']
#     else:
#         poster_url = None
#
#     # Create a message with the movie details and poster
#     movie_msg = f"<b>🎬 {movie['title']}</b> ({movie['year']})\n\n"
#     movie_msg += f"<b>⭐️ Rating:</b> {movie['rating']}\n"
#     movie_msg += f"<b>🎭 Genres:</b> {' | '.join(movie['genres'])}\n\n"
#     movie_msg += f"📝: {movie['plot'][0]}...\n"
#
#     # Create inline keyboard with two buttons
#     view_button = InlineKeyboardButton(text="View on IMDb", url=f"https://www.imdb.com/title/tt{movie.getID()}/")
#     more_details_button = InlineKeyboardButton(text="More Details", callback_data=f"more_details {movie.getID()}")
#
#     # Add the buttons to an InlineKeyboardMarkup object
#     keyboard = InlineKeyboardMarkup([[view_button], [more_details_button]])
#
#     # Send the message with the poster and button_list
#     await callback_query.message.reply_photo(
#         photo=poster_url,
#         caption=movie_msg,
#         reply_markup=keyboard,
#     )
#     await callback_query.message.delete()


# Define the callback query handler for the "More Details" button
@Client.on_callback_query(filters.regex("^more_details"))
async def more_details_handler(client, callback_query):
    # Get the IMDb ID of the movie from the callback data
    imdb_id = callback_query.data.split(" ")[1]
    await callback_query.answer("Ok")
    back = callback_query.data.split(":")[1]
    movie = ia.get_movie(imdb_id)
    # Create a message with the movie details
    movie_msg = f"<b>🎬 {movie.get('title')}</b> ({movie.get('year')})\n\n"
    movie_msg += f"<b>⭐️ Rating:</b> {movie.get('rating')}\n"
    movie_msg += f"<b>🎭 Genres:</b> {' | '.join(movie.get('genres', []))}\n"
    movie_msg += f"<b>🌐 Language:</b> {' | '.join(movie.get('languages', []))}\n"
    movie_msg += f"<b>⏱️ Runtime:</b> {movie.get('runtimes', [])} minutes\n"
    movie_msg += f"<b>📝 Plot:</b> {movie.get('plot', [''])}...\n"
    movie_msg += "\n<b>🌟 Cast:</b>\n"

    # Add the cast members to the message
    for person in movie.get('cast', [])[:5]:
        movie_msg += f"- {person.get('name')} ({person.get('currentRole')})\n"

    # Send the message with the movie Details
    view_button = InlineKeyboardButton(text="View on IMDb", url=f"https://www.imdb.com/title/tt{movie.getID()}/")
    back_button = InlineKeyboardButton(text="Back", url=f"back_to_search:{back}")
    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup([[view_button], [back_button]])
    await callback_query.message.edit_text(
        text=movie_msg,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@Client.on_callback_query(filters.regex("^back_to_search"))
async def back_to_search_handler(client, callback_query):
    movie_name = callback_query.data.split(":")[1]
    await callback_query.answer(movie_name)
    movies = ia.search_movie(movie_name, results=10)
    # Create a list of buttons for each search result
    button_list = []
    for i, movie in enumerate(movies[:10]):
        button_list.append(
            [InlineKeyboardButton(text=f"{movie['title']} ({movie['year']})",
                                  callback_data=f"more_details {movie.movieID}")]
        )

    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup(button_list)

    # Send a message to the user with the search results and buttons
    message_text = f"Found {len(movies)} results. Please select a movie:"
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
    await callback_query.message.delete()

from imdb import IMDb 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

# import pyrogram.types.
ia = IMDb()


@Client.on_callback_query(filters.regex("^\d+\.more_details.*"))
async def more_details_handler(client, callback_query):
      imdb_id = int(callback_query.data.split(" ")[1])
      await callback_query.answer("Hold on..", show_alert=True)
      back = callback_query.data.split(":")[1]
      movie = ia.get_movie(imdb_id)
  
      if 'full-size cover url' in movie.keys():
          poster_url = movie['full-size cover url']
      elif 'cover url' in movie.keys():
          poster_url = movie['cover url']
      else:
          poster_url = "https://exchange4media.gumlet.io/news-photo/123661-93930-IMDbAmazon.jpg"
  
      # Formatting and displaying movie details
      movie_msg = f"🎬 **Title:** {movie.get('title')}\n"
      movie_msg += f"📅 **Year:** {movie.get('year')}\n"
  
      # Rating
      try:
          rating = movie.get('rating')
          movie_msg += f"⭐️ **Rating:** {rating}" if rating else "⭐️ **Rating:** N/A"
          movie_msg += "\n"
      except KeyError:
          movie_msg += "⭐️ **Rating:** N/A\n"
  
      # Genres
      try:
          genres = movie.get('genres', [])
          movie_msg += f"🎭 **Genres:** {', '.join(genres)}" if genres else "🎭 **Genres:** N/A"
          movie_msg += "\n"
      except KeyError:
          movie_msg += "🎭 **Genres:** N/A\n"
  
      # Languages
      try:
          languages = movie.get('languages', [])
          movie_msg += f"🌐 **Languages:** {', '.join(languages)}" if languages else "🌐 **Languages:** N/A"
          movie_msg += "\n"
      except KeyError:
          movie_msg += "🌐 **Languages:** N/A\n"
  
      # Runtime
      try:
          runtime = movie.get('runtimes', ['N/A'])[0]
          movie_msg += f"⏱️ **Runtime:** {runtime} minutes" if runtime else "⏱️ **Runtime:** N/A"
          movie_msg += "\n"
      except (KeyError, IndexError):
          movie_msg += "⏱️ **Runtime:** N/A\n"
  
      # Plot
      try:
          plot = movie.get('plot', [''])[0]
          movie_msg += f"📝 **Plot:** {plot}..." if plot else "📝 **Plot:** N/A"
          movie_msg += "\n"
      except (KeyError, IndexError):
          movie_msg += "📝 **Plot:** N/A\n"
  
      # Directors
      try:
          directors = [director.get('name') for director in movie.get('director', [])]
          movie_msg += f"🎥 **Directors:** {', '.join(directors)}\n"
      except KeyError:
          movie_msg += "🎥 **Directors:** N/A\n"
  
      # Writers
      try:
          writers = [writer.get('name') for writer in movie.get('writer', [])]
          movie_msg += f"🖋️ **Writers:** {', '.join(writers)}\n"
      except:
          movie_msg += "🖋️ **Writers:** N/A\n"
  
      # Cast
      movie_msg += "\n🌟 **Cast:**\n"
      for person in movie.get('cast', [])[:5]:
          try:
              name = person.get('name', 'N/A')
              role = person.get('currentRole', 'N/A')
              movie_msg += f"- {name} ({role})\n"
          except KeyError:
              movie_msg += "- N/A\n"
  
      # Streaming Platforms
      streaming_info = movie.get('akas', [])
      if streaming_info:
          movie_msg += "\n📺 **Streaming As:**\n"
          for entry in streaming_info:
              movie_msg += f"- {entry}\n"
  
      # Release Dates
      release_dates = movie.get('release dates', {})
      if release_dates:
          movie_msg += "\n🗓️ **Release Dates:**\n"
          for country, date in release_dates.items():
              movie_msg += f"- {country}: {date}\n"
      # Send the message with the movie Details
      view_button = InlineKeyboardButton(text="View on IMDb", url=f"https://www.imdb.com/title/tt{movie.getID()}/")
      back_button = InlineKeyboardButton(text="Back", callback_data=f"{callback_query.from_user.id}.back_to_search:{back}")
      # Add the buttons to an InlineKeyboardMarkup object
      keyboard = InlineKeyboardMarkup([[view_button], [back_button]])
      # await message.reply_to_message.edit_media(
      #     media=InputMediaPhoto("https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg", caption="satya"))
      await callback_query.message.edit_media(
          media=InputMediaPhoto(poster_url, caption=movie_msg),
          # text=movie_msg,
          # disable_web_page_preview=True,
          reply_markup=keyboard,
      )

@Client.on_callback_query(filters.regex("^\d+\.back_to_search.*"))
async def back_to_search_handler(client, callback_query):
    if (int(callback_query.data.split(".")[0])) != (int(callback_query.from_user.id)):
        await callback_query.answer('This is not for you!', show_alert=True)
        return
    movie_name = callback_query.data.split(":")[1]
    await callback_query.answer(movie_name, show_alert=True)
    movies = ia.search_movie(movie_name, results=10)
    # Create a list of buttons for each search result
    button_list = []
    for i, movie in enumerate(movies[:10]):
        button_list.append(
            [InlineKeyboardButton(text=f"{movie['title']}",
                                  callback_data=f"{callback_query.from_user.id}.more_details {movie.movieID} :{movie_name}:")]
        )

    # Add the buttons to an InlineKeyboardMarkup object
    keyboard = InlineKeyboardMarkup(button_list)

    # Send a message to the user with the search results and buttons
    message_text = f"Found {len(movies)} results. Please select a movie:"
    await callback_query.message.edit_media(
        media=InputMediaPhoto("https://exchange4media.gumlet.io/news-photo/123661-93930-IMDbAmazon.jpg", caption=message_text),
        # text=message_text,
        reply_markup=keyboard,
        # disable_web_page_preview=True
    )

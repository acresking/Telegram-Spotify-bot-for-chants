import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                                                 client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")))

def start(update, context):
    update.message.reply_text('Hello! Send me a Spotify song link and I will send it back as a music file.')

def convert_to_music(update, context):
    try:
        user_message = update.message.text

        if user_message.startswith("https://open.spotify.com") or user_message.startswith("http://open.spotify.com"):
            track_id = user_message.split('/')[-1].split('?')[0] 

            track_info = spotify.track(track_id)

            track_name = track_info.get('name')

            preview_url = track_info.get('preview_url')

            if preview_url:
                context.bot.send_audio(chat_id=update.message.chat_id, audio=preview_url, title=track_name)
            else:
                update.message.reply_text("Sorry, I couldn't find the preview for this song.")
        else:
            pass
    except SpotifyException as e:
        update.message.reply_text("Error: Unable to fetch track information from Spotify.")
    except Exception as e:
        update.message.reply_text("An unexpected error occurred. Please try again later.")

def main():
    updater = Updater(token=os.getenv("API_TOKEN"), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_to_music))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

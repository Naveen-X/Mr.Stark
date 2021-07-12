import os
import time
import pyrogram
import logging

from Stark.config import Config

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


if __name__ == "__main__" :

    print("Starting Assistant...")
    plugins = dict(root="Stark/Plugins")
    app = pyrogram.Client(
        "Mr.stark",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    app.run()

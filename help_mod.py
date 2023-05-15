class Script(object):
    AI = [
        {
            "desc": "Generates AI response from OpenAI",
            "cmds": ["gpt", "askgpt", "chatgpt"],
            "usage": "/gpt Who are you?"
        },
        {
            "desc": "Generates images using OpenAI",
            "cmds": ["generate", "genimage"],
            "usage": "/genimage an alien"
        }
    ]
    CARBON = [
        {
            "desc": "Creates a carbon in doc format",
            "cmds": ["carbon"],
            "usage": "/carbon reply to a text message or give some text as input"
        },
        {
            "desc": "Creates a carbon in image format",
            "cmds": ["icarbon"],
            "usage": "/carbon reply to a text message or give some text as input"
        }
    ]
    DEV = [
        {
            "desc": "Executes python code",
            "cmds": ["eval", "e"],
            "usage": "/e <python code>"
        },
        {
            "desc": "Run bash/terminal cmd",
            "cmds": ["bash", "sh"],
            "usage": "/bash <cmd>"
        }
    ]
    FUN = [
        {
            "desc": "Get a cat image",
            "cmds": ["cat"],
        },
        {
            "desc": "Get a dog image",
            "cmds": ["dog"],
        },
        {
            "desc": "Get a random meme",
            "cmds": ["meme"],
        },
        {
            "desc": "Get a panda image",
            "cmds": ["panda"],
        }
    ]
    GOOGLE = [
        {
            "desc": "Google searcher!",
            "cmds": ["gs", "google"],
            "usage": "/gs <text to search>"
        },
    ]
    INSTADL = [
        {
            "desc": "Download post/reel from instagram",
            "cmds": ["insta", "instadl", "insdl", "instadownload"],
            "usage": "/instadl <instagram post/reel link>"
        }
    ]
    LOGOS = [
        {
            "desc": "Makes a logo for you with black bg",
            "cmds": ["alogo"],
            "usage": "/alogo <text for logo>"
        },
        {
            "desc": "Makes a logo for you, try it out",
            "cmds": ["slogo"],
            "usage": "/slogo <text for logo>"
        }
    ]
    MISC = [
        {
   "desc": "Add chat to quote db",
   "cmds": ["ad_qt"],
   "usage": "/add_qt"
        },
        {
   "desc": "remove chat from quote db",
   "cmds": ["del_qt"],
   "usage": "/del_qt"
        },
        {
   "desc": "sends quote daily at 8:00 am and 6:00 pm",
   "cmds": ["no cmd"],
   "usage": "works automatically"
        }
    ]
    PORT = [
        {
            "desc": "Scans open ports of an ip address",
            "cmds": ["scanip"],
            "usage": "/scanip <domain/ip>"
        }
    ]
    PASTE = [
        {
            "desc": "Pastes the given text in spacebin",
            "cmds": ["paste"],
            "usage": "/paste <reply to message/text file>"
        }
    ]
    QR = [
        {
            "desc": "Generates qr for given text",
            "cmds": ["qr"],
            "usage": "/qr <text to make qr>"
        }
    ]
    QUOTLY = [
        {
            "desc": "Converts your text into a quote",
            "cmds": ["quote", "qt", "qu", "q"],
            "usage": "/q <reply to a text message>"
        }
    ]
    STICKER = [
        {
            "desc": "Creates a sticker with given text",
            "cmds": ["stcr"],
            "usage": "/stcr Mr.Stark"
        }
    ]
    SYSTEM = [
        {
            "desc": "Ping-Pong",
            "cmds": ["p", "ping"],
        },
        {
            "desc": " whether the bot is alive or not",
            "cmds": ["alive"],
        },
        {
            "desc": "Restarts the bot",
            "cmds": ["restart"],
        }
    ]
    TELEGRAPH = [
        {
            "desc": "Creates a telegraph",
            "cmds": ["/telegraph", "/tgraph"],
            "usage": "/tgraph <title for the telegraph | reply to a text message>"
        }
    ]
    TRANSLATE = [
        {
            "desc": "Translates the replied message",
            "cmds": ["tr", "translate"],
            "usage": "/tr <language code | reply to a text message>"
        }
    ]
    UPDATE = [
        {
            "desc": "Updates the system",
            "cmds": ["up", "update"],
        },
        {
            "desc": "Deletes snippets in gitlab",
            "cmds": ["d"],
        }
    ]
    URLUPLOADER = [
        {
            "desc": "download's file from given link",
            "cmds": ["urlupload"],
            "usage": "/urlupload [direct link of the file]"
        }
    ]
    WASTED = [
        {
            "desc": "Gta-V wasted effect on replied image",
            "cmds": ["wasted"],
            "usage": "/wasted <reply to a photo>"
        }
    ]
    WHOIS = [
        {
            "desc": "Know who the replied person is",
            "cmds": ["info", "whois"],
            "usage": "/info <user id/username | reply to a user message"
        }
    ]
    WRITE = [
        {
            "desc": "Writes given text on a white paper",
            "cmds": ["write"],
            "usage": "/write hello"
        }
    ]

#Credits to CatUB
#Originally made in telethon ny @feelded
#Ported to Pyrogram by @Naveen_xD

import os
import re
import time
import random
import base64
import requests
import contextlib
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from Stark import error_handler
from Stark.config import Config
from pyrogram import Client, filters

THEMES = [
    "breeze",
    "candy",
    "crimson",
    "falcon",
    "meadow",
    "midnight",
    "raindrop",
    "sunset",
]

MODES = ["mode-day", "mode-night"]

class chromeDriver:
    @staticmethod
    def start_driver():
        if Config.CHROME_BIN is None:
            return None, "Need to install Google Chrome or Chromium. Module Stopping."
        try:
            chrome_options = ChromeOptions()
            chrome_options.binary_location = Config.CHROME_BIN
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--test-type")
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--disable-gpu")
            prefs = {"download.default_directory": "./"}
            chrome_options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(options=chrome_options)
            return driver, None
        except Exception as err:
            return None, str(err)

    @staticmethod
    def bypass_cache(inputstr, driver=None):
        if driver is None:
            driver, error = chromeDriver.start_driver()
            if not driver:
                return None, error
        driver.get(inputstr)
        if "google" in inputstr:
            with contextlib.suppress(Exception):
                driver.find_element(By.ID, "L2AGLb").click()
            with contextlib.suppress(Exception):
                driver.find_element(
                    By.XPATH, "//button[@aria-label='Accept all']"
                ).click()
        return driver, None

    @staticmethod
    def get_html(inputstr):
        driver, error = chromeDriver.bypass_cache(inputstr)
        if not driver:
            return None, error
        html = driver.page_source
        driver.close()
        return html, None

    @staticmethod
    def get_rayso(
        inputstr, file_name="Rayso.png", title="Mr.Stark", theme="crimson", darkMode=True
    ):
        url = f'https://ray.so/#code={base64.b64encode(inputstr.encode()).decode().replace("+","-")}&title={title}&theme={theme}&padding=64&darkMode={darkMode}&language=python'
        driver, error = chromeDriver.start_driver()
        if error:
            return None, error
        driver.set_window_size(2000, 20000)
        driver.get(url)
        element = driver.find_element(By.CLASS_NAME, "Controls_controls__kwzcE")
        driver.execute_script("arguments[0].style.display = 'none';", element)
        frame = driver.find_element(By.CLASS_NAME, "Frame_frame__Dmfe9")
        frame.screenshot(file_name)
        driver.quit()
        return file_name, None

    @staticmethod
    async def get_screenshot(inputstr, message=None):
        start = datetime.now()
        driver, error = chromeDriver.bypass_cache(inputstr)
        if not driver:
            return None, error
        if message:
            x = await message.reply_text(
                "`Calculating Page Dimensions with Google Chrome BIN`"
            )
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        driver.set_window_size(width + 100, height + 100)
        im_png = driver.get_screenshot_as_png()
        if message:
            await x.edit("`Stoppping Chrome Bin`")
        driver.close()
        end = datetime.now()
        ms = (end - start).seconds
        return im_png, f"**url : **{inputstr} \n**Time :** `{ms} seconds`"

def text_chunk_list(query, bits=29900):
    text_list = []
    string = query
    checker = len(query)
    if checker > bits:
        limit = int(checker / (int(checker / bits) + 1))
        string = ""

        for item in query.split(" "):
            string += f"{item} "
            if len(string) > limit:
                string = string.replace(item, "")
                text_list.append(string)
                string = ""
    if string != "":
        text_list.append(string)
    return text_list


@Client.on_message(filters.command("Rayso"))
@error_handler
async def rayso_by_pro_odi(c, m):
    "To paste text or file into image."
    files = []
    captions = []
    reply_to_id = m.reply_to_message.id
    try:
      query = m.text.split(None, 1)[1]
    except IndexError:
      query = None
    if m.reply_to_message:
      rquery = m.reply_to_message.id
    else:
      rquery = None
    rayso = await m.reply_text("**Processing...**")
    checker = query.split(maxsplit=1) if query else None
    # Add Theme
    if checker and (checker[0].lower() in THEMES or checker[0].lower() == "random"):
        if checker[0] == query and not rquery:
            return await rayso.edit("`Theme changed to {query.title()}.`")
        query = checker[1] if len(checker) > 1 else None

    # Add Mode
    # if checker and checker[0].lower() in MODES:
    #     if checker[0] == query and not rquery:
    #         return await edit_delete(
    #             catevent, f"`Theme Mode changed to {query.title()}.`"
    #         )
    #     query = checker[1] if len(checker) > 1 else None

    # Themes List
    if query == "-l":
        ALLTHEME = "**🎈Modes:**\n**1.**  `Mode-Day`\n**2.**  `Mode-Night`\n\n**🎈Themes:**\n**1.**  `Random`"
        for i, each in enumerate(THEMES, start=2):
            ALLTHEME += f"\n**{i}.**  `{each.title()}`"
        return await rayso.edit(ALLTHEME)

    # Get Theme
    theme = checker or "random"
    if theme == "random":
        theme = random.choice(THEMES)

    # Get Mode
    mode = random.choice(MODES)
    darkMode = mode == "mode-night"

    if query:
        text = query
    elif rquery:
        if rquery.document and rquery.document.mime_type.startswith("text"):
            filename = await rquery.download()
            with open(filename, "r") as f:
                text = str(f.read())
            os.remove(filename)
        elif rquery.text:
            text = rquery.txt
        else:
            return await rayso.edit("`Unsupported.`")
    else:
        return await rayso.edit("`What should I do?`")

    # // Max size 30000 byte but that breaks thumb so making on 28000 byte
    text_list = text_chunk_list(text, 28000)
    user = m.from_user.first_name
    for i, text in enumerate(text_list, start=1):
        await rayso.edit(f"**Making Rayso Image: {i}/{len(text_list)} **")
        outfile, error = chromeDriver.get_rayso(
            text, file_name=f"rayso{i}.png", title=user, theme=theme, darkMode=darkMode
        )
        if error:
            return await rayso.edit(error)
        files.append(outfile)
        captions.append("")

    await rayso.edit("**📎 Uploading... **")
    captions[-1] = f"<i>➥ Generated by : <b>{m.from_user.mention}</b></i>"
    await c.send_document(
        m.chat.id,
        files,
        reply_to=reply_to_id,
        force_document=True,
        caption=captions,
    )
    await rayso.delete()
    for name in files:
        os.remove(name)
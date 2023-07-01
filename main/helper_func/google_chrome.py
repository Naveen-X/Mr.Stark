import base64
import contextlib
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from Stark.config import Config


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
        inputstr, darkMode:bool, file_name="Rayso.png", title="Mr.Stark", theme="crimson"
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

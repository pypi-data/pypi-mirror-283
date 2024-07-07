from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")


def webdriver_maker(remote_url: str = None, headless: bool = True, no_sandbox: bool = True):
    # options
    options = Options()
    if headless:
        options.add_argument("--headless")
    if no_sandbox:
        options.add_argument("--no-sandbox")

    # remote driver
    if remote_url:
        raise NotImplementedError

    # self driver
    chrome_driver_manager = ChromeDriverManager()
    chrome_driver_path = chrome_driver_manager.install()
    return webdriver.Chrome(options=options, service=Service(chrome_driver_path))

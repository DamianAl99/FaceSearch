from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
import chromedriver_autoinstaller
import time

class DriverHelper:
    def __init__(self, webUrl, debug_mode):
        self.webUrl = webUrl
        self.debug_mode = debug_mode
        self.driver = self.initDriver()

    def initDriver(self):
        options = Options()
        options.add_experimental_option("detach", True)
        chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

        options.add_argument("no-sandbox")
        options.headless = self.debug_mode
        driver = webdriver.Chrome(options= options)
        driver.get(self.webUrl)
        driver.set_window_size(1296,696)
        return driver

    def buscarPorXpath(self, xpath: str, timeout: int=0) -> WebElement:
        time.sleep(timeout)
        return self.driver.find_element("xpath", xpath)

    def buscarXPorXpath(self, xpath: str, timeout: int=0):
        time.sleep(timeout)
        return self.driver.find_elements("xpath", xpath)

    def escribirEnInput(self, elementoXpath: WebElement, escribirValor):
        return elementoXpath.send_keys(escribirValor)

    def htmlDeLaPagina(self) -> str:
        time.sleep(5)
        return self.driver.page_source

    def ejecutarJs(self, script: str):
        return self.driver.execute_script(script)

    def cerrar_ventantas(self):
        self.driver.quit()

    def existe_elemento(self, xpath: str, timeout = 0) -> bool:
        time.sleep(timeout)
        try:
            self.driver.find_element("xpath", xpath)
            return True
        except:
            return False

    def common(self):
        return self.driver

    def web_driver(self):
        return webdriver



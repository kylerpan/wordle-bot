from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
import time

class wait_for_not_data_state(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            return element.get_attribute('data-state') != self.text
        except EC.StaleElementReferenceException:
            return False

options = Options()
# options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.nytimes.com/games/wordle/index.html")
# playButton.click()

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'purr-blocker-card__button'))).click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="Play"]'))).click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="icon-close"]'))).click()

for char in "tares":
  driver.find_element(By.CSS_SELECTOR, f'button[data-key="{char}"]').click()
driver.find_element(By.CSS_SELECTOR, 'button[data-key="↵"]').click()

rowNum = 1
WebDriverWait(driver, 10).until(wait_for_not_data_state((By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]/div[5]/div'), 'tbd'))

row = driver.find_element(By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]')
chars = row.find_elements(By.CSS_SELECTOR, 'div[class="Tile-module_tile__UWEHN"]')
for char in chars:
  print(char.get_attribute('data-state'))


time.sleep(1000)
driver.quit()
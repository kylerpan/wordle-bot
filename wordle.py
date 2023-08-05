#
# Solves the wordle of the day in browser
# using selenium
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from expectedValues import changeValidWords
from messenger import messenger

POSSIBLE_WORDS = [f'{line.rstrip()}' for line in open("textFiles/possibleWords.txt", "r")]
INITIAL_EXPECTED_VALUE = [tuple(line.rstrip().split(', ')) for line in open("textFiles/initialExpectedValue.txt", "r")]

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
        
# TODO: change these values to fit your needs
shareResults = True # if you want to share your results with someone on messenger
                    # if True, then change values in messenger.py too
        
def main():
  options = Options()
  # options.add_experimental_option("detach", True)

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  driver.get("https://www.nytimes.com/games/wordle/index.html")

  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'purr-blocker-card__button'))).click()
  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="Play"]'))).click()
  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="icon-close"]'))).click()

  rowNum = 1
  wordsLeft = POSSIBLE_WORDS
  wordsLeftExpected = INITIAL_EXPECTED_VALUE
  while (rowNum < 7):
    # picking word
    word = wordsLeftExpected[0][0]
    print(f'Chosen word: {word}')
    for char in word:
      driver.find_element(By.CSS_SELECTOR, f'button[data-key="{char}"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[data-key="↵"]').click()

    # wait for tiles to flip over
    WebDriverWait(driver, 10).until(wait_for_not_data_state((By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]/div[5]/div'), 'tbd'))

    # getting the state of tiles
    row = driver.find_element(By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]')
    chars = row.find_elements(By.CSS_SELECTOR, 'div[class="Tile-module_tile__UWEHN"]')
    states = []
    for char in chars:
      states.append(char.get_attribute('data-state'))

    # getting words left with stats
    wordsLeftExpected, wordsLeft = changeValidWords(word, states, wordsLeft)

    try:
      share = driver.find_element(By.XPATH, '/html/body/div/div/dialog/div/div/div/div[4]/div[2]/div/button')
      print(f'The word is "{wordsLeft[0]}"')
      break
    except EC.NoSuchElementException:
      pass

    print('\nHere are some words with the highest amount of information after picking {word}:')
    for i in range(15):
      print(wordsLeftExpected[i][0], f'{wordsLeftExpected[i][1]}' + '0' * (18 - len(str(wordsLeftExpected[i][1]))))
    print()

    rowNum += 1

  messenger(driver)
  driver.quit()

if __name__ == '__main__':
    main()
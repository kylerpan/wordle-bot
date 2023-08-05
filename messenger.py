#
# Shares the results of solving wordle and 
# sends it to a person on messenger
#

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# TODO: change these values to fit your needs
link = 'https://www.messenger.com' # link to the person you want to send a message too
username = 'username' # username for messenger account
password = 'password' # password for messenger account


def messenger(driver):
  # sharing results in messenger
  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/dialog/div/div/div/div[4]/div[2]/div/button'))).click()
  driver.get(link)

  # login
  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/input[7]')))
  webEmail = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/input[7]')
  webPassword = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/input[8]')
  signIn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div/div[3]/div/div/form/div/div[1]/button')

  webEmail.send_keys(username)
  webPassword.send_keys(password)
  signIn.click()

  # type into text box
  WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')))
  textBox = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
  textBox.send_keys(Keys.COMMAND + 'v')
  textBox.send_keys(Keys.ENTER)

  time.sleep(5)
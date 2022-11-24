from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import pandas as pd
from tqdm import tqdm
import time
from sys import exit



# No GUI test
#options = Options()
#options.add_argument("--headless")  # testing

# Initialize data and the driver
print("[INITIALIZING...]")
data= {"lnk":[], "id":[]}
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Connecting to the provided league
print("Connecting...")
driver.get("https://www.sofascore.com/") 
print("Connection established!")

# Scrolling down to the all leagues
# ! FIX THIS: Generalize scrolling to the right button in order for the program to find it [FIXED]
# ? Check if it works over multiple screen sizes
def checkElement():
    try:
        driver.find_element(By.XPATH, "//div[text()='All leagues']").click()
        return True
    except:
        return False

step = 0 # Control the scrolling pace
# Scroll until the Matches Section appears to be clickable
while True:
    step += 500
    driver.execute_script("window.scrollTo(0, {})".format(step))
    driver.implicitly_wait(3)
    if checkElement():
        break
    else:
        continue

driver.implicitly_wait(2)

print("\n[READY]")
print("Getting links...")

links = {'lnk': []}
countries = driver.find_elements(By.XPATH, "//span[@class='sc-eDWCr LNyIs']") # countries list
for country in countries: # for each country
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", country) # focus on each
    country.click() # open up the relative leagues
    leagues = driver.find_elements(By.XPATH, "//div[@class='sc-hLBbgP gOkXmD']//a") # get leagues list
    for league in leagues: # for each league
        links['lnk'].append(league.get_attribute('href')) # get the link
        print(league.get_attribute('href'))
    country.click()
    time.sleep(2)


print("\nWriting file: ./data/links/all_leagues.csv")
df = pd.DataFrame(links)
df.to_csv("./data/links/all_leagues.csv", index=False)
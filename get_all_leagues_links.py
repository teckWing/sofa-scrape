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
countries = driver.find_elements(By.XPATH, "//span[@class='sc-eDWCr LNyIs']") # lista paesi
for country in countries: # per ogni paese
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", country)
    country.click() # apro la lista dei campionati
    leagues = driver.find_elements(By.XPATH, "//div[@class='sc-hLBbgP gOkXmD']//a") # ottengo la lista dei campionati
    for league in leagues: # per ogni campionato
        links['lnk'].append(league.get_attribute('href')) # ottengo il link classico da dare in pasto a get_matches_links.py
        print(league.get_attribute('href'))
    country.click()
    time.sleep(2)

    #step += 20
    #driver.execute_script("window.scrollTo(0, {})".format(step))


print("\nWriting file: ./data/links/all_leagues.csv")
df = pd.DataFrame(links)
df.to_csv("./data/links/all_leagues.csv", index=False)


exit(0)

# For each league day, get all matches links
for i in tqdm(range(0, int(args.rounds)-1)):
    matches=driver.find_elements(By.XPATH, "//div[@class='sc-hLBbgP hBOvkB']/a ")
    #print(matches) # uncomment for troubleshooting
    
    for x in matches:
        data["lnk"].append(x.get_attribute("href"))
        data["id"].append(x.get_attribute("data-id"))
    driver.find_element(By.XPATH, "//span[text()='Previous']").click()  

# Final output
df = pd.DataFrame(data)

fout = "./data/links/{}_{}.csv".format(args.output, str(args.season).replace("/", "_"))
print("\nWriting file: {}".format(fout))
df.to_csv(fout, index=False)

print("\n[FINISHED]")
print("Run get_matches_stats.py for scraping player and teams statistics.\n")
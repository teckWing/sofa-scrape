from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import pandas as pd
from tqdm import tqdm
from sys import exit

# Defining command line arguments
parser = argparse.ArgumentParser(description='Get links for a given league.')
parser.add_argument("--league", help="A link to a league.", default="")
parser.add_argument("--season", help="Season to scrape in the AA/AA format. Example: 21/22", default="21/22")
parser.add_argument("--output", help="The name of the output file.", default="matches_links")
parser.add_argument("--rounds", help="The number of rounds in the given season.", default="38")
args = parser.parse_args()

# Check whether a link has been passed 
if args.league == "":
    print("A link to a league must be provided!")
    print("Use the --league argument.")
    print("Example: --league https://www.sofascore.com/tournament/football/spain/laliga/8")
    exit(0)

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
driver.get(args.league) 
print("Connection established!")

# Selecting the season provided as input
print("\nPositioning")
driver.find_element(By.XPATH,'//button/div/span[text()="22/23"]').click()
season=args.season
driver.find_element(By.XPATH,"//li[text()="+"'"+season+"']").click()

# Scrolling down to the league days
# ! FIX THIS: Generalize scrolling to the right button in order for the program to find it [FIXED]
# ? Check if it works over multiple screen sizes
def checkElement():
    try:
        driver.find_element(By.XPATH, "//div[text()=\"By Round\"]").click()
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
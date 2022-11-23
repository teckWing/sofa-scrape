from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from tqdm import tqdm


options = Options()
options.add_argument("--headless")  # comment it to run with normal way

data= {"lnk":[], "id":[]}
#driver = webdriver.Chrome('chromedriver.exe')
#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# collego a sofa serie A (per altro campionato sostituire il link)
print("Connecting...")
driver.get('https://www.sofascore.com/tournament/football/spain/laliga/8')
print("Connection established!")
# apro menù a tendina con stagioni disponibili
print("Positioning")
driver.find_element(By.XPATH,'//button/div/span[text()="22/23"]').click()
# seleziono stagione
season="21/22"
driver.find_element(By.XPATH,"//li[text()="+"'"+season+"']").click()
# scrollo fino alle giornate e aspetto per far caricare
try:
    driver.execute_script("window.scrollTo(0, 1000)") 
    driver.implicitly_wait(3)
    
    # clicco per ottenere le partite per giornata
    driver.find_element(By.XPATH, "//div[text()=\"By Round\"]").click()
except:
    driver.execute_script("window.scrollTo(0, 1000)") 
    driver.implicitly_wait(3)

    # clicco per ottenere le partite per giornata
    driver.find_element(By.XPATH, "//div[text()=\"By Round\"]").click()



print("[READY]")
print("Getting links...")

for i in tqdm(range(0,37)):
    #matches=driver.find_elements(By.XPATH, "//div[@class='sc-hKwDye gtOvrf']/a ")
    matches=driver.find_elements(By.XPATH, "//div[@class='sc-hLBbgP hBOvkB']/a ")
    #print(matches) # uncomment for troubleshooting
    for x in matches:
        data["lnk"].append(x.get_attribute("href"))
        data["id"].append(x.get_attribute("data-id"))
    driver.find_element(By.XPATH, "//span[text()='Previous']").click()  


df = pd.DataFrame(data)

print("Writing file: data/matches_link.csv")
df.to_csv("./data/matches_link.csv", index=False)

print("[FINISHED]")
print("Run ...py for getting stats.")
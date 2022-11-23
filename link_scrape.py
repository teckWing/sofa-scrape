from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


data= {"lnk":[], "id":[]}
driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()

# collego a sofa serie A (per altro campionato sostituire il link)
driver.get('https://www.sofascore.com/tournament/football/spain/laliga/8')
# apro menù a tendina con stagioni disponibili
driver.find_element(By.XPATH,'//button/div/span[text()="22/23"]').click()
# seleziono stagione
season="21/22"
driver.find_element(By.XPATH,"//li[text()="+"'"+season+"']").click()
# scrollo fino alle giornate e aspetto per far caricare
driver.execute_script("window.scrollTo(0, 2000)") 
driver.implicitly_wait(3)
# clicco per ottenere le partite per giornata
driver.find_element(By.XPATH, "//div[text()=\"By Round\"]").click()

for i in range(0,37):
    matches=driver.find_elements(By.XPATH, "//div[@class='sc-hKwDye gtOvrf']/a ")
    for x in matches:
        data["lnk"].append(x.get_attribute("href"))
        data["id"].append(x.get_attribute("data-id"))
    driver.find_element(By.XPATH, "//span[text()='Previous']").click()  


df = pd.DataFrame(data)

df.to_csv("link_partite.csv", index=False)
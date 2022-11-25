from genericpath import isfile
from requests import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm
from sys import exit
import os



def get_summary_stats(driver, save):
    player_names = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[2]"
    )

    player_goals = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[3]")
    player_assists = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[4]")

    player_minutes = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[10]"
    )
    player_position = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[11]"
    )

    player_rating = driver.find_elements(By.XPATH,
        "//table//span[@class='sc-eDWCr kODVra']"
    )

    player_objects = list()
    for i in range(len(player_names)):
        player_objects.append(
            [player_names[i].text, player_goals[i].text, player_assists[i].text, player_minutes[i].text, player_position[i].text,
             player_rating[i].get_attribute("innerHTML")]
        )

    players = pd.DataFrame(player_objects)
    players.columns = ['Player', "Goals", "Assists",'Minutes', 'Position', 'Rating']
    if save:
        players.to_csv('summaryStats.csv', sep=',', line_terminator='\n', index=False)
        print('Summary stats collected successfully')
    else:
        print('Summary stats collected successfully')
        return players


def get_attacking_stats(driver, save):
    driver.find_element(By.XPATH,"//*[text()='Attack']").click()
    player_names = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[2]"
    )

    player_shots_on = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[3]")
    
    player_shots_off = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[4]")
    
    player_shots_blc = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[5]")

    player_dribbles_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[6]")
    
    player_notes = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[7]")
    

    player_objects = list()
    for i in range(len(player_names)):
        player_dribbles, player_successful_dribbles = player_dribbles_info[i].text.split('(')
        player_dribbles = player_dribbles[:-1]
        player_successful_dribbles = player_successful_dribbles[:-1]
        player_objects.append(
            [player_names[i].text, player_shots_on[i].text, player_shots_off[i].text, player_shots_blc[i].text,
             player_dribbles, player_successful_dribbles,
              player_notes[i].text])
    players = pd.DataFrame(player_objects)
    players.columns = ['Player', 'Shots on target', 'Shots off target', 'Shots blocked', 'Dribbles',
                       'Successful dribbles', 'Notes (Attacking)']
    if save:
        players.to_csv('attackingStats.csv', sep=',', line_terminator='\n', index=False)
        print('Attacking stats collected successfully')
    else:
        print('Attacking stats collected successfully')
        return players


def get_defending_stats(driver, save):
    driver.find_element(By.XPATH,"//*[text()='Defence']").click()
    player_names = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[2]"
    )
    player_clearances = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[3]")
    player_shots_blocked = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[4]")
    player_interceptions = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[5]")
    player_tackles = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[6]")
    player_dribbledpast= driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[7]")
    player_notes = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[8]")
    
    player_objects = list()
    for i in range(len(player_names)):
        player_objects.append([player_names[i].text, player_clearances[i].text, player_shots_blocked[i].text,
                               player_interceptions[i].text, player_tackles[i].text, player_dribbledpast[i].text,player_notes[i].text])
    players = pd.DataFrame(player_objects)
    players.columns = ['Player', 'Clearances', 'Blocked shots', 'Interceptions', 'Tackles',"Dribbled Past" ,'Notes (Defending)']
    if save:
        players.to_csv('defendingStats.csv', sep=',', line_terminator='\n', index=False)
        print('Defending stats collected successfully')
    else:
        print('Defending stats collected successfully')
        return players


def get_passing_stats(driver, save):
    driver.find_element(By.XPATH,"//*[text()='Passing']").click()
    player_names = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[2]"
    )
    player_touches = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[3]"
    )
    player_passes_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[4]")
    player_key_passes = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[5]")
    player_crosses_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[6]")
    player_long_balls_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[7]")
    player_notes = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[8]")
    

    player_objects = list()
    for i in range(len(player_names)):
        try:
            player_passes, player_pass_accuracy = player_passes_info[i].text.split('(')
            player_passes_corr,player_passes_tot = player_passes.split("/")
            player_pass_accuracy = player_pass_accuracy[:-2]
        except:
            player_passes_corr= 0
            player_passes_tot= 0
            player_pass_accuracy = np.nan

        player_crosses, player_crosses_successful = player_crosses_info[i].text.split('(')
        player_crosses = player_crosses[:-1]
        player_crosses_successful = player_crosses_successful[:-1]
        player_long_balls, player_long_balls_successful = player_long_balls_info[i].text.split('(')
        player_long_balls = player_long_balls[:-1]
        player_long_balls_successful = player_long_balls_successful[:-1]
        player_objects.append([player_names[i].text,player_touches[i].text, player_passes_corr, player_passes_tot, player_pass_accuracy,
                               player_key_passes[i].text,
                               player_crosses, player_crosses_successful,
                               player_long_balls, player_long_balls_successful, player_notes[i].text])
    players = pd.DataFrame(player_objects)
    players.columns = ['Player', "Touches",'Accurate Passes', "Tot. Passes", 'Pass accuracy', 'Key passes', 'Crosses', 'Successful crosses', 'Long balls', 'Successful long balls',
                       'Notes (Passing)']
    if save:
        players.to_csv('passingStats.csv', sep=',', line_terminator='\n', index=False)
        print('Passing stats collected successfully')
    else:
        print('Passing stats collected successfully')
        return players


def get_duel_stats(driver, save):
    driver.find_element(By.XPATH,"//*[text()='Duels']").click()
    player_names = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[2]"
    )

    player_gduels_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[3]")
    player_aduels_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[4]")
    
    player_dispossessed = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[5]")
    player_fouled = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[7]")
    player_fouls = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[6]")
    player_offside = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[8]")
    
    player_objects = list()
    for i in range(len(player_names)):
        player_gduels, player_gduels_won = player_gduels_info[i].text.split('(')
        player_gduels = player_gduels[:-1]
        player_gduels_won = player_gduels_won[:-1]
        player_aduels, player_aduels_won = player_aduels_info[i].text.split('(')
        player_aduels = player_aduels[:-1]
        player_aduels_won = player_aduels_won[:-1]
        player_objects.append([player_names[i].text, player_gduels, player_gduels_won, player_aduels, player_aduels_won,
                            player_dispossessed[i].text, player_fouled[i].text, player_fouls[i].text, player_offside[i].text])
    players = pd.DataFrame(player_objects)
    players.columns = ['Player', 'Ground Duels', 'Ground Duels won','Aerial Duels', 'Aerial Duels won', 'Dispossessions', 'Fouled', 'Fouls', 'Offside']
    if save:
        players.to_csv('duelStats.csv', sep=',', line_terminator='\n', index=False)
        print('Duel stats collected successfully')
    else:
        print('Duel stats collected successfully')
        return players


def get_goalkeeping_stats(driver, save):
    driver.find_element(By.XPATH,"//*[text()='Goalkeeper']").click()
    player_names = driver.find_elements(By.XPATH,
        "//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[2]"
    )

    player_saves = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[3]")
    player_punches = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[4]")
    player_run_outs_info = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[5]")
    player_high_claims = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[6]")
    player_notes = driver.find_elements(By.XPATH,"//table[@class='sc-dIfARi cmjpkd'] /tbody/tr/td[7]")

    player_objects = list()
    for i in range(len(player_names)):
        player_run_outs, player_run_outs_successful = player_run_outs_info[i].text.split('(')
        player_run_outs = player_run_outs[:-1]
        player_run_outs_successful = player_run_outs_successful[:-1]
        player_objects.append([player_names[i].text, player_saves[i].text, player_punches[i].text,
                               player_run_outs, player_run_outs_successful, player_high_claims[i].text,
                               player_notes[i].text])
    players = pd.DataFrame(player_objects)
    players.columns = ['Player', 'Saves', 'Punches', 'Run-outs',
                       'Successful run-outs', 'High claims',
                       'Notes (Goalkeeping)'
                       ]
    if save:
        players.to_csv('goalkeepingStats.csv', sep=',', line_terminator='\n',index=False)
        print('Goalkeeping stats collected successfully')
    else:
        print('Goalkeeping stats collected successfully')
        return players


def collect_data(driver):
    summary_stats = get_summary_stats(driver, False)

    attacking_stats = get_attacking_stats(driver, False)
    matches = [item for item in summary_stats.columns if item in attacking_stats.columns]
    total_stats = pd.merge(summary_stats, attacking_stats, on=matches)

    defending_stats = get_defending_stats(driver, False)
    matches = [item for item in total_stats.columns if item in defending_stats.columns]
    total_stats = pd.merge(total_stats, defending_stats, on=matches)
    
    passing_stats = get_passing_stats(driver, False)
    matches = [item for item in total_stats.columns if item in passing_stats.columns]
    total_stats = pd.merge(total_stats, passing_stats, on=matches)

    duel_stats = get_duel_stats(driver, False)
    matches = [item for item in total_stats.columns if item in duel_stats.columns]
    total_stats = pd.merge(total_stats, duel_stats, on=matches)

    goalkeeping_stats = get_goalkeeping_stats(driver, False)
    total_stats = pd.merge(total_stats, goalkeeping_stats, on='Player', how='outer')
    total_stats.replace(np.nan, '-', inplace=True)

    fout = "./data/stats/{}.csv".format(args.output)
    print("Writing update to: ", fout)
    if os.path.isfile(fout)==True:
        total_stats.to_csv(fout, 
                           sep=',', 
                           lineterminator='\n', 
                           encoding='utf-8', 
                           index=False, 
                           mode="a", 
                           header=False)
    else:
        total_stats.to_csv(fout, 
                           sep=',', 
                           lineterminator='\n',
                           encoding='utf-8', 
                           index=False)



# Defining command line arguments
parser = argparse.ArgumentParser(description='Get stats for a given matches links.')
parser.add_argument("--links", help="The name of the file containing matches link.", default="")
parser.add_argument("--output", help="The name of the output file.", default="stats_league")
args = parser.parse_args()

# Check whether the given matches links exists.
if os.path.isfile("./data/links/{}.csv".format(args.links)) == False:
    print("A file containing matches links must be provided!")
    print("Make sure it exists and it is located in data/links/.")
    print("Use the --links argument.")
    print("Example: --links links_laliga_20_21")
    exit(0)

print("File found!")
print("[INITIALIZING...]")

# No GUI test
#options = Options()
#options.add_argument("--headless")  # ! testing

# Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.maximize_window()

# Read the given file
df = pd.read_csv("./data/links/{}.csv".format(args.links))
print("File loaded.")

print("[READY]\n")
for r in df.iloc():
    id = str(r['id'])
    custom= r['lnk'].split("/")[-1]
    s = 'window.localStorage.setItem("sofa.event.details.load-id",JSON.stringify({"eventId":'+ id+', "customId":"'+custom+'"}));'
    driver.get(r["lnk"])
    driver.execute_script(s)
    driver.execute_script("location.reload();")
    driver.implicitly_wait(5)

    print("Collecting: ", r['lnk'])

    driver.find_element(By.XPATH,"//div[text()='Player statistics']").click()
    collect_data(driver)

    print("\n")
    #try:
    #    driver.find_element(By.XPATH,"//div[text()='Player statistics']").click()
    #    collect_data(driver)
    #except:
    #    continue
    
driver.quit()
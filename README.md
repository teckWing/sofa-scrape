# A sofascore.com scraper.

Build your football database and analyze it from both exploratory and inferential perspectives.  
⚽️📈

<p align="left">
  <a href="">
    <img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2022" target="_blank" />
  </a>
  
  <a href="">
    <img alt="Contributors" src="https://img.shields.io/github/contributors/lorenzotrcnl/sofa-scrape" target="_blank" />
  </a>  
</p>

## Features

✅ Constantly updated with the current version of the website  
✅ Get performances stats about all the players in a match  
✅ Easy to use  
❌ Only scraping data from past seasons  

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Internet Connection
- Chrome
- Python 3.6+

## Usage
``` sh
> python get_matches_links.py -h  
usage: get_matches_links.py [-h] [--league LEAGUE] [--season SEASON] [--output OUTPUT] [--rounds ROUNDS]

Get links for a given league.

options:
  -h, --help       show this help message and exit
  --league LEAGUE  A link to a league.
  --season SEASON  Season to scrape in the AA/AA format. Example: 21/22
  --output OUTPUT  The name of the output file.
  --rounds ROUNDS  The number of rounds in the given season.
```

``` sh
> python get_matches_stats.py -h  
usage: get_matches_stats.py [-h] [--links LINKS] [--output OUTPUT]

Get stats for a given matches links.

options:
  -h, --help       show this help message and exit
  --links LINKS    The name of the file containing matches link.
  --output OUTPUT  The name of the output file.

```


## Quickstart
Clone this repo using:

``` sh
> git clone https://github.com/lorenzotrcnl/sofa-scrape && cd sofa-scrape
```
  
Install the required packages using:

``` sh
> pip install -r requirements.txt
```
  
Go to [sofascore.com](https://sofascore.com) and search for the league of interest. Note down the link and the number of rounds in the season.  
Execute the command below by passing the respective arguments, for example:

``` sh
> python get_matches_links.py \
    --league https://www.sofascore.com/tournament/football/spain/laliga/8 \
    --output links_laliga \
    --season 20/21 \
    --rounds 38
```

Now in ```data/links``` will be created the file containing the list of matches links.  
This will be used by the next command to scroll through the various matches and extract the statistics of each one.

> **Note**: the final output name will be the combination of --output and --season, so in the previous command it will be ```links_laliga_20_21```.

Finally, to extract all the stats of each individual player in each match run the following command:

``` sh
> python get_matches_stats.py \
    --links links_laliga_20_21 \
    --output stats_laliga_20_21
```

The output file will be created in ```data/stats```.
  
## 🚧 To-Do
- [ ] Add what match player's stats belongs to
- [ ] Add round variable in player's stats
- [ ] Implement scraping of the current season

Feel free to propose improvements and contribute to the repo.
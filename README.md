# A sofascore.com scraper.

With this scraper yuo can extract stats regarding teams and player on the official Sofascore website.  
Aligned with its current html structure.

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
usage: 

```


## Quickstart
Clone this repo using:

``` sh
> git clone https://github.com/lorenzotrcnl/sofa-scrape
```

Go to [sofascore.com](https://sofascore.com) and search for the league of interest. Note down the link and the number of rounds in the season.  
Execute the command below by passing the respective arguments, for example:

``` sh
> python get_matches_links.py \
    --league https://www.sofascore.com/tournament/football/spain/laliga/8 \
    --output links_laliga \
    --season 21/22 \
    --rounds 38
```

Now in ```data/links``` the file containing the matches links has been created.  
This will be used by the next command to scroll through the various matches and extract the statistics of each one.
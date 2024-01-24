# CS:GO Skin Webscraper using selenium

Scrape the steam market for the current prices of csgo skins and get results stored in a csv file
It uses tkinter for a "native" gui and selenium for webscraping. \

[Screenshot of the GUI](docs/gui.png)

## Disclaimers

This is an old project that I only revived to the point where it is working again, but it is very scrappy. \

- It runs very slowly due to the nature of fully simulating the brower. But I thought it was necessary as skins are loaded dynamically. As of Janurary 2024 you can simply query <https://steamcommunity.com/market/search/render> with `norender=1` which is a lot faster.
- Once you press "Scrape" the GUI becomes unresponsive, as the codebase is entirely synchronous.
- A lot of feedback is only given via the console, instead of the GUI
- Seemingly randomly the error "There was an error performing your search. Please try again later." occurs, which seems to be steams way of blocking bot requests.
- probably many more issues...

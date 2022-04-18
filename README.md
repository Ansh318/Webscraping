# Treasure Hunt

I have created a web scraper to find lost secrets! This web scraper
is contained in a module called a file called `scrape.py` which contains
one class called  `Scraper`.

# Website

You'll be scraping a website implemented as a flask application. Selenium to perform the webscraping. To
run it, I have used the relevant html, csv, and css files and `application.py`.

# Overview

The link to the website is `http://<IP>:5000`.

Each page (under "ENTER THE MAZE") contains information in the form of
a letter. Either a DFS or BFS search through the site and
concatenatination of letters from the pages in the order in which they're
visited, will result in a password. DFS buttons are for a DFS
search and the BFS buttons are for a BFS search.

By performing both searches, you'll get two passwords.  Entering
either correct password on the home page will redirect you to a
different page.




# Commands to run the module

```python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrape import Scraper

#kill previous chrome instance if still around (to conserve memory)
os.system("pkill chrome")

url = "http://VM_IP:5000" # TODO: enter your VM's IP
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
s = Scraper(driver, url)

print("Easter Egg:", s.easter_egg())

dpass = s.dfs_pass()
print("\nDFS Password", dpass)

bpass = s.bfs_pass()
print("\nBFS Password", bpass)

print("\nDFS Locations")
print(s.protected_df(dpass))

print("\nBFS Locations")
print(s.protected_df(bpass))

s.driver.close()
```

## Authors

- [@AnshAgarwal](https://www.github.com/Ansh318)


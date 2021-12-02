
"""
cinema.py
Find data from listchallenges and return csv file in data directory
Author: Anthony Chatfield

The page shown at the link below contains movies with some metadata of interest to our friend Quentin, a budding movie director.

https://www.listchallenges.com/100-must-see-movies-for-more-advanced-cinephiles

title
year
ranking
no_of_votes


Task
Using your preferred language and/or tools - write a program that parses this page and extracts the following data into two possible file formats

1 - A CSV file
2 - A HTML file with some style formatting applied - You can use a CSS framework like https://tailwindcss.com/docs to complete this task.


Include instructions on how to run your program including installing any dependencies.

Usage:

python cinema.py --format [ CSV | HTML ]

"""
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

#define paths for chrome.exe and chromedriver.exe
chrome_path = "C:\Program Files\Google\Chrome\Application\Chrome.exe"
chromedriver_path = "C:\Windows\chromedriver"
service = Service(chromedriver_path)

#define webdriver options
chrome_options = webdriver.ChromeOptions()
#specify chrome options
chrome_options.binary_location = chrome_path
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def getSoup(wd, website):
		"""get html content of a website"""
		wd.get(website)
		return BeautifulSoup(wd.page_source, 'html.parser')

def movieAndYear(input):
		"""Gets (Movie, Year) from ""movie (year)" string input"""
		return (input[:-7], int(input[-6:][1:5]))

def getMoviesFromSite(wd, website):
  """scrapes listchallenges stats website for movies in list"""
  movies = []
  soup = getSoup(wd, website+"/vote")
  for a in soup.findAll('div', "listVote-item small-tall"):
    #get title, strip whitespace
    title = a.find('div', "item-name").text.strip()
    movieYear = movieAndYear(title) #separate title and year
    #get rank, take away #
    rank = int(a.find('td', "listVoteItem-rank").text.strip()[1:])
    #get num of up and down votes and add together
    no_of_votes = int(a.find('span', "listVote-upVoteCount").text.strip()) + int(a.find('span', "listVote-downVoteCount").text.strip())
    movies.append({'title': movieYear[0], 'year': movieYear[1],
    'rank': rank, 'votes': no_of_votes})
  return movies

def transform(website):
  #try to instantiate driver and get movies list of dictionaries
  try:
    wd = webdriver.Chrome(service=service, options=chrome_options) # , desired_capabilities=capabilities)
    movies = getMoviesFromSite(wd, website)
  finally:
    #if error, quit the driver
    wd.quit()
  moviesdf = pd.DataFrame(movies)
  moviesdf.set_index('rank')
  return moviesdf
  
if __name__ == "__main__":
  website = "https://www.listchallenges.com/100-must-see-movies-for-more-advanced-cinephiles"
  df = transform(website)
  #convert to csv file
  df.to_csv('data/cinema.csv')


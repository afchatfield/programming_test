
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

Dependencies:
This script uses selenium to web scrape using a chromedriver, link to installation guide is here:
https://selenium-python.readthedocs.io/installation.html

The script also uses beautiful soup and pandas but those are simpler and more common packages
if these are not installed, a simple `pip install [package]` should work to install it to your machine
otherwise refer to installation and usage guides for respective packages

"""
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import getopt, sys

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
    movies.append({'Title': movieYear[0], 'Year': movieYear[1],
    'Rank': rank, 'Votes': no_of_votes})
  return movies

def transform(website):
  #try to instantiate driver and get movies list of dictionaries
  try:
    wd = webdriver.Chrome(service=service, options=chrome_options) # , desired_capabilities=capabilities)
    movies = getMoviesFromSite(wd, website)
  finally:
    #if error, quit the driver
    wd.quit()
  moviesdf = pd.DataFrame(movies).set_index('Rank')
  return moviesdf
  
def main(argv):
  try:
    options, _ = getopt.getopt(argv,"f:", longopts=["format="])
  except getopt.GetoptError:
    print('Error with options')
    sys.exit(2)
  format = ""
  for opt, arg in options:
    if opt == "--format":
      format = arg
      break
    elif opt == "-f":
      format = arg
      break
    else:
      print("Wrong Option")
      sys.exit(2)
  website = "https://www.listchallenges.com/100-must-see-movies-for-more-advanced-cinephiles"
  df = transform(website)
  if format.lower() == 'csv':
    # convert to csv file
    df.to_csv('data/cinema.csv')
  elif format.lower() == 'html':
    # convert to html file
    html = df.to_html()
    html = html[:93] + "Rank" + html[93:] # add rank to first heading
    html = html[:174] + html[261:] # remove second heading onverted from dataframe
    # add html to file
    with open("data/cinema.html", "w") as f:
      f.write("""<html>
      <head>
        <link rel="stylesheet" href="cinema.css">
      </head>
      <body>\n""" +
          html +
      """\n</body>
      </html>""")

if __name__ == "__main__":
  main(sys.argv[1:])


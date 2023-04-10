import requests
from bs4 import BeautifulSoup
import re

#URL = input("\nInput announcements url:\n")
URL = "https://www.smore.com/gd9uc"

def collectWebsite(Url):
  page = requests.get(Url) 
  soup = BeautifulSoup(page.content, "html.parser")
  results = soup.find(id="w-4074839830") 
  job_elements = results.find_all("td", class_="gallery-content-cell") # type: ignore
  return job_elements[0].text.strip()

def formatWebsitePeople(input):
  listOfPeople = []
  for item in re.split(r"\d+.\d+...", input):
    statement = re.sub(r"( and)", ",", item)
    if str(re.match(r"(This week we celebrate...)", statement)) == "None":
      listOfPeople.append(statement)
      print(statement)
  return(listOfPeople)

def formatWebsiteDate(input):
  return re.search(r"\d+.\d+", input).group() # type: ignore

data = collectWebsite(URL)
print()
print(formatWebsiteDate(data))
formatWebsitePeople(data)
print()
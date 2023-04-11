import requests
from bs4 import BeautifulSoup
import re

URL = input("\nInput announcements url:\n")
if URL == "":
  URL = "https://www.smore.com/6rj5s"

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
      #print(statement)
  return(listOfPeople)

def splitPeople(input):
  peoplesList = []
  outList = []
  for day in input:
    peoplesList = []
    for person in re.split(r"(,)", day):
      if person != ",":
        peoplesList.append(person)
        # print(person)
    outList.append(peoplesList)
    # print("\n--Next day--\n")
  return outList


def formatWebsiteDate(input):
  return re.search(r"\d+.\d+", input).group() # type: ignore

data = collectWebsite(URL)
print()
print(formatWebsiteDate(data))
for a in splitPeople(formatWebsitePeople(data)):
  print(a)
# for dayPeople in formatWebsitePeople(data):
  # print(dayPeople)
print()
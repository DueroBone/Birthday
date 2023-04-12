import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from datetime import date
import os.path

login = open("Login", "r").read().splitlines()

URL = ""
if os.path.exists("AnnouncementsSave") == False:
    URL = input("\nInput announcements url:\n")
    if URL == "":  
        URL = "https://www.smore.com/6rj5s"


def collectWebsite(Url):
    if os.path.exists("AnnouncementsSave") == True:
        print("Loading save file...")
        return open("AnnouncementsSave", "r").read()
    page = requests.get(Url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="w-4074839830")
    job_elements = results.find_all("td", class_="gallery-content-cell")  # type: ignore
    return job_elements[0].text.strip()


def formatWebsitePeople(input):
    listOfPeople = []
    for item in re.split(r"\d+.\d+...", input):
        statement = re.sub(r"( and)", ",", item)
        if str(re.match(r"(This week we celebrate...)", statement)) == "None":
            listOfPeople.append(statement)
    return (listOfPeople)


def splitPeople(input):
    peoplesList = []
    outList = []
    for day in input:
        peoplesList = []
        for person in re.split(r"(,)", day):
            if person != ",":
                peoplesList.append(person)
        outList.append(peoplesList)
    return outList


def formatWebsiteDate(input):
    return re.search(r"\d+.\d+", input).group()  # type: ignore


def findTodayPeople(dateIn, peoplesList):
    today = date.today()
    thisYear = today.strftime("%Y")
    dateFormat = "%m/%d/%Y"
    dateSplit = re.split(r"(/)", dateIn)
    startDay = datetime.strptime(f'{dateSplit[0]}/{dateSplit[2]}/{date.today().year}', dateFormat)
    today = datetime.strptime(str(today), "%Y-%m-%d")
    daysSinceStart = (today - startDay).days
    return(f"{peoplesList[daysSinceStart]}")


def getPeople():
    return [findTodayPeople(formatWebsiteDate(data), formatWebsitePeople(data))]

def convertToEmails(input):
    print()


def emailPeople(message, people):
    username = login[0]
    password = login[1]

## Where the code actually runs
data = collectWebsite(URL)
print(getPeople())
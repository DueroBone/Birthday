import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

login = open("Login", "r").read().splitlines()

URL = input("\nInput announcements url:\n")
if URL == "":
    URL = "https://www.smore.com/6rj5s"


def collectWebsite(Url):
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
            # print(statement)
    return (listOfPeople)


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
    return re.search(r"\d+.\d+", input).group()  # type: ignore


def findTodayPeople(date, peoplesList):
    dateSplit = re.split(r"(/)", date)
    startDay = date(2023, dateSplit[0], dateSplit[1])
    #datetime.striptime()


def emailPeople(message, people):
    username = login[0]
    password = login[1]


data = collectWebsite(URL)
print()
print(formatWebsiteDate(data))
for a in splitPeople(formatWebsitePeople(data)):
    print(a)
# for dayPeople in formatWebsitePeople(data):
    # print(dayPeople)
print()
print(f"User: {login[0]} Pass: {login[1]}")
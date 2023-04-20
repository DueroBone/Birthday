import requests
import re
import os.path
import smtplib
import ssl
import sys
import validators
from bs4 import BeautifulSoup
from datetime import datetime, date

login = open("Login", "r").read().splitlines()


def Quit():
    print("Canceling...")
    sys.exit()


URL = ""
if os.path.exists("AnnouncementsSave") == False:
    URL = input("Input announcements url:  ")
    if URL == "" or validators.url(URL) != True or re.match(r"(smore)", URL) == []:
        print(f"Improper input detected!! {URL}")
        Quit()


def collectWebsite(Url):
    if os.path.exists("AnnouncementsSave") == True:
        print("Loading save file...")
        return open("AnnouncementsSave", "r").read()
    page = requests.get(Url)
    print("Working", end="")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="w-4074839830")
    job_elements = results.find_all(
        "td", class_="gallery-content-cell")  # type: ignore
    print(".", end="")
    return job_elements[0].text.strip()


def formatWebsitePeople(input):
    listOfPeople = []
    for item in re.split(r"\d+.\d+...", input):
        statement = re.sub(r"( and)", ",", item)
        if str(re.match(r"(This week we celebrate...)", statement)) == "None":
            listOfPeople.append(statement)
    print(".", end="")
    return listOfPeople


def splitPeople(input):
    peoplesList = []
    outList = []
    for day in input:
        peoplesList = []
        for person in re.split(r"(,)", day):
            if person != ",":
                peoplesList.append(person)
        outList.append(peoplesList)
    print(".", end="")
    return outList


def formatWebsiteDate(input):
    return re.search(r"\d+.\d+", input).group()  # type: ignore


def findTodayPeople(dateIn, peoplesList):
    today = datetime.today()
    # print(today)
    thisYear = today.year
    dateFormat = "%m/%d/%Y"
    dateSplit = re.split(r"(/)", dateIn)
    startDay = datetime.strptime(
        f'{dateSplit[0]}/{dateSplit[2]}/{date.today().year}', dateFormat)
    daysSinceStart = (today - startDay).days
    print(".", end="")
    return (peoplesList[daysSinceStart])


def getPeopleWeb():
    return findTodayPeople(formatWebsiteDate(data), splitPeople(formatWebsitePeople(data)))


def convertToEmails(inputE):
    emailsList = []
    for person in inputE:
        person = str(person).replace(" ", "").lower() + "@danville.k12.in.us"
        if re.match(r"(mr)", str(person)) != "None" and re.match(r"(mrs)", str(person)) != "None" and re.match(r"(ms)", str(person)) != "None" and re.findall(r"(no)", person) == []:
            emailsList.append(person)
        else:
            response = input(
                f"\nPerson is: {person}, please type in email address\n")
            if response != "":
                emailsList.append(response)

    print(".", end="")
    return emailsList


def emailPeople(people):
    if input(f"\nSending to: {people}\nPress enter to continue") != "":
        Quit()
    username = login[0]
    password = login[1]
    port = 587  # For starttl
    smtp_server = "smtp.gmail.com"
    message = """Subject: To you
Happy birthday!
    """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(username, password)
        server.sendmail(username, people, message)


# Where the code actually runs
data = collectWebsite(URL)
emailPeople(convertToEmails(getPeopleWeb()))

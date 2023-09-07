import requests
import re
import sys
import validators
from bs4 import BeautifulSoup
from datetime import datetime, date        

login = open("Login", "r").read().splitlines()


def _Quit():
    print("Canceling...")
    sys.exit()


def _collectWebsite():
    if len(sys.argv) == 2:
        Url = sys.argv[1]
        if Url == "" or validators.url(Url) != True or re.match(r"(smore)", Url) == []:
            print(f"Improper input detected!! {Url}")
            _Quit()
    else:
        print("Do offline stuff")
        _Quit()
    page = requests.get(Url) # type: ignore
    print("Working", end="")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="w-2338593074")
    job_elements = results.find_all(class_="gallery-content-cell")  # type: ignore
    print(".", end="")
    input(job_elements[0])

    # if os.path.exists("AnnouncementsSave") == False:
        # savefile = open("AnnouncementsSave", "w")
        # savefile.write(job_elements[0].text.strip())
    return job_elements[0].text.strip()


def _formatWebsitePeople(input):
    listOfPeople = []
    for item in re.split(r"\d+.\d+...", input):
        statement = re.sub(r"( and)", ",", item)
        if str(re.match(r"(This week we celebrate...)", statement)) == "None":
            listOfPeople.append(statement)
    print(".", end="")
    return listOfPeople


def _splitPeople(input):
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


def _formatWebsiteDate(input):
    return re.search(r"\w+.\d+.(-)", input).group()  # type: ignore


def _findTodayPeople(dateIn, peoplesList):
    today = datetime.today()
    # print(today)
    thisYear = today.year
    dateFormat = "%m/%d/%Y"
    dateSplit = re.split(r"(/)", date.strftime(dateIn, "%B %d"))
    startDay = datetime.strptime(
        f'{dateSplit[0]}/{dateSplit[2]}/{date.today().year}', dateFormat)
    daysSinceStart = (today - startDay).days
    print(".", end="")
    return peoplesList[daysSinceStart]


def _getPeopleWeb(data):
    output:list[str] = _findTodayPeople(_formatWebsiteDate(data), _splitPeople(_formatWebsitePeople(data)))
    return output


# Where the code actually runs
def gatherWebsite():
    return _getPeopleWeb(_collectWebsite())
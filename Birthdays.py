import requests, re, os.path, smtplib, ssl, sys
from bs4 import BeautifulSoup
from datetime import datetime, date

login = open("Login", "r").read().splitlines()

URL = ""
if os.path.exists("AnnouncementsSave") == False:
    URL = input("\nInput announcements url:\n")
    if URL == "":  
        URL = "https://www.smore.com/vwf04"
    print()


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
    return outList


def formatWebsiteDate(input):
    return re.search(r"\d+.\d+", input).group()  # type: ignore


def findTodayPeople(dateIn, peoplesList):
    today = datetime.today()
    # print(today)
    thisYear = today.year
    dateFormat = "%m/%d/%Y"
    dateSplit = re.split(r"(/)", dateIn)
    startDay = datetime.strptime(f'{dateSplit[0]}/{dateSplit[2]}/{date.today().year}', dateFormat)
    daysSinceStart = (today - startDay).days
    # print(f"today{today.day}, start{startDay.day}, {daysSinceStart}")
    return(peoplesList[daysSinceStart])


def getPeople():
    return findTodayPeople(formatWebsiteDate(data), splitPeople(formatWebsitePeople(data)))

def convertToEmails(inputE):
    # print(re.split(r"(, )", str().join(str(input))))
    emailsList = []
    for person in inputE:
        if re.match(r"(Mr)", str(person)) != "None" and re.match(r"(Mrs)", str(person)) != "None" and re.match(r"(Ms)", str(person)) != "None":
            person = str(person).replace(" ", "").lower() + "@danville.k12.in.us"
            emailsList.append(person)
    return(emailsList)


def emailPeople(people):
    if input(f"Sending to: {people}\n Press enter to continue") != "":
        sys.exit()
    username = login[0]
    password = login[1]
    port = 587  # For starttl
    smtp_server = "smtp.gmail.com"
    sender_email = username
    receiver_email = people
    message = """Subject: To you
Happy birthday!
    """
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

## Where the code actually runs
data = collectWebsite(URL)
emailPeople(convertToEmails(getPeople()))
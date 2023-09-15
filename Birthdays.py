import re
import smtplib
import ssl
import sys
from datetime import datetime
from importFiles import updateZip
from parseWebsite import gatherWebsite
import mySecretsFile as msf


isHeadless = sys.argv == "HEADLESS"


def Quit(input = None):
    print(input) if input != None else print("Canceling...")
    sys.exit()


def convertToEmails(inputE: list[str]):
    emailsList: list[str] = []
    for person in inputE:
        # add mailing domain then check if is valid
        person = str(person).replace(" ", "").lower() + msf.var2
        if re.match(r"(mr)", str(person)) != "None" and re.match(r"(mrs)", str(person)) != "None" and re.match(r"(ms)", str(person)) != "None" and re.findall(r"(no)", person) == []:
            emailsList.append(person)
        else:
            # if not valid, ask for user input
            response = input(
                f"\nPerson is: {person}, please type in email address\n")
            if response != "":
                emailsList.append(response)

    print(".", end="")
    return emailsList


def gettoday():
    for data in msf.database:
        if (datetime.today().date() - data[0]).days % 365 == 0:  # type: ignore
            return data[1]
    return "None"


def emailPeople(people: list[str]):
    if people == "None":
        Quit()
    if input(f"\nSending to: {people}\nPress enter to continue") != "":
        Quit()
    username = msf.var8
    password = msf.pass1
    port = 587
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()

    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)
    server.login(username, password)
    server.sendmail(username, people, msf.message)
    server.close()


# Where the code actually runs
if __name__ == "__main__":
    updateZip()
    if isHeadless:
        emails:list[str] = gettoday() # type: ignore
    else:
        # update database
        emails = convertToEmails(gatherWebsite())
    emailPeople(emails)
    updateZip()

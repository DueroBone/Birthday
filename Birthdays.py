import re
import os.path
import smtplib
import ssl
import sys
from importFiles import decryptFiles, updateSecrets
from parseWebsite import gatherWebsite


login = open("Login", "r").read().splitlines()


def Quit():
    print("Canceling...")
    sys.exit()


def convertToEmails(inputE:list[str]):
    emailsList:list[str] = []
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


def emailPeople(people: list[str]):
    if input(f"\nSending to: {people}\nPress enter to continue") != "":
        Quit()
    username = login[0]
    password = login[1]
    port = 587  # For starttl
    smtp_server = "smtp.gmail.com"
    message = open("messages").read()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(username, password)
        server.sendmail(username, people, message)


# Where the code actually runs
if __name__ == "__main__":
    if not os.path.exists("Database.txt"):
        if not os.path.isdir("emlFiles"):
            decryptFiles()
    # check for argv, if exists, update db with link, if not, run headless
    emailPeople(convertToEmails(gatherWebsite()))
    updateSecrets()
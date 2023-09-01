import email
import json
import re
import os.path
from datetime import datetime
import pyzipper
from zipfile import ZipFile

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def getPass():
    return open("Login").readlines()[1].strip().join(open("Login").readlines()[3].strip()).encode('utf-8')

def getFiles():
    folder = "emlFiles"
    return [email.message_from_bytes(open(file, "rb").read()) for file in [f"{folder}/{subdir}/{file}" for subdir in os.listdir(f"{folder}") for file in os.listdir(f"{folder}/{subdir}")]]


def stripEmailsFiles():
    output = ""
    for daysEmail in getFiles():
        if not daysEmail["Bcc"] and not daysEmail["To"]:
            continue
        allAddresses = re.findall(regex, (daysEmail["Bcc"] + daysEmail["To"] if daysEmail["Bcc"] and daysEmail["To"] else daysEmail["Bcc"] if daysEmail["Bcc"] else daysEmail["To"]))
        mailDate = daysEmail["Date"]

        if "REDACTED" not in allAddresses: # put in personal email address
            output += str([str(datetime.strptime(str(mailDate).replace(" (PDT)", ""), "%a, %d %b %Y %H:%M:%S %z").date()), str(json.dumps(allAddresses))]).replace("\'", "\"") + "\n"  # type: ignore
    return output



def importFiles():
    if not os.path.exists("Database.txt"):
        if os.path.exists("Secrets.zip"):
            pyzipper.AESZipFile("Secrets.zip", "r", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES).extractall(pwd=getPass())
        else:
            if os.path.isdir("emlFiles"):
                open("Database.txt", "w").write(stripEmailsFiles())
                print("Saved as Database.txt")
            else:
                ZipFile("emlFiles.zip").extractall("emlFiles", pwd=getPass())
                importFiles()

def updateSecrets():
    try:
        os.remove("Secrets.zip")
    except:
        1 == 1
    zf = pyzipper.AESZipFile("Secrets.zip", "x", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES)
    zf.setpassword(getPass())
    # zf.write("Login")
    zf.write("Database.txt")
    zf.write("emlFiles.zip") if os.path.exists("emlfiles.zip") else 1 == 1
    zf.close()

if __name__ == "__main__":
    importFiles()
    updateSecrets()
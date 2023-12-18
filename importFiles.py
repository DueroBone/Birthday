import email
import json
import re
import os.path
from datetime import datetime
import pyzipper
from zipfile import ZipFile
try:
    import mySecretsFile as msf
except:
    raise FileNotFoundError(
        "You need to have the secrets file to access this program!!")


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def _getPass():
    return msf.pass1.strip().join(msf.pass2.strip()).encode('utf-8')


# for original parsing of .eml files || left in for sake of studying

def _getFiles():
    folder = "emlFiles"
    return [email.message_from_bytes(open(file, "rb").read()) for file in [f"{folder}/{subdir}/{file}" for subdir in os.listdir(f"{folder}") for file in os.listdir(f"{folder}/{subdir}")]]


def _stripEmailsFiles():
    output = ""
    for daysEmail in _getFiles():
        if not daysEmail["Bcc"] and not daysEmail["To"]:
            continue
        allAddresses = re.findall(regex, (daysEmail["Bcc"] + daysEmail["To"] if daysEmail["Bcc"]
                                  and daysEmail["To"] else daysEmail["Bcc"] if daysEmail["Bcc"] else daysEmail["To"]))
        mailDate = daysEmail["Date"]

        if msf.var8 not in allAddresses:
            output += str([str(datetime.strptime(str(mailDate).replace(" (PDT)", ""), "%a, %d %b %Y %H:%M:%S %z").date()),
                          str(json.dumps(allAddresses))]).replace("\'", "\"") + "\n"  # type: ignore
    return output


# for reading Database.txt
# left encrypted because I shouldn't really put that on github

def _unZip():
    print("Unzipping files...", end="")
    pyzipper.AESZipFile("Secrets.zip", "r", compression=pyzipper.ZIP_LZMA,
                        encryption=pyzipper.WZ_AES).extractall(pwd=_getPass())
    print(" done!")


def _decryptFiles():
    if not os.path.exists("mySecretsFile.py"):
        if os.path.exists("Secrets.zip"):
            _unZip()
        else:
            if os.path.isdir("emlFiles"):
                open("Database.txt", "w").write(_stripEmailsFiles())
                print("Saved as Database.txt")
            elif os.path.exists("emlFiles.zip"):
                ZipFile("emlFiles.zip").extractall("emlFiles", pwd=_getPass())
                _decryptFiles()
            else:
                raise PermissionError(
                    "Haha, you tried to access things that you don't have access to!!")
    else:
        if not hasattr(msf, "saveMe") or not bool(msf.saveMe):
            _unZip()


def _updateSecrets():

    os.remove("Secrets.zip") if os.path.exists("Secrets.zip") else None
    zf = pyzipper.AESZipFile(
        "Secrets.zip", "x", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES)
    zf.setpassword(_getPass())
    zf.write("mySecretsFile.py")
    zf.write("Database.txt")
    zf.close()


def updateZip():
    _decryptFiles()
    _updateSecrets()


if __name__ == "__main__":
    updateZip()

import mySecretsFile as msf
from datetime import timedelta, datetime

import sys
# print([data if (datetime.today().date() - data[0]).days%365 == 0 else None for data in msf.database]) # type: ignore


def gettoday():
    for data in msf.database:
        if (datetime.today().date() - data[0]).days % 365 == 0:  # type: ignore
            return data
    return [datetime.today(), ["None"]]


print(gettoday()[1])
print(len(sys.argv))
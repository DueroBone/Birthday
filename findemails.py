import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
emails = re.findall(regex, open("Database.txt").read())
print(emails)
print(len(emails))

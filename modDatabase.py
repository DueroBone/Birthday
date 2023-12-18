import re
import mySecretsFile as msf

database = open("Database.txt").read().splitlines()
# output = []
# for line in database:
#   dates = re.findall(r"(?<=-)\d\d(?!\d)", re.findall(r"\"\d+-\d+-\d+\"", line).__str__())
#   emails = re.findall(msf._regex, line)
#   out = dates[0] + " " + dates[1] + " "
#   for email in emails:
#     out += email + " "
#   output.append(out)

# outputs = []
# for thing in output:
#   if not re.findall(r"\d\d \d\d", thing)[0] in outputs:
#     outputs.append(thing)

# outputs.sort()
# for thing in outputs:
#   print(thing)

output = []
for line in database:
  dates = re.findall(r"(?<=-)\d\d(?!\d)", re.findall(r"\"\d+-\d+-\d+\"", line).__str__())
  emails = re.findall(msf._regex, line)
  out = dates[0] + " " + dates[1] + " "
  for email in emails:
    out += email + " "
  output.append(out)

outputs = []
for thing in output:
  if not re.findall(r"\d\d \d\d", thing)[0] in outputs:
    outputs.append(thing)

outputs.sort()
for thing in outputs:
  print(thing)
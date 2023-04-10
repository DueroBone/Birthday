import re
input = "This week we acelebrate..."
print(str(re.match(r"(This week we celebrate...)", input)) == "None")
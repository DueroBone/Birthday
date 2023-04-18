import re
words = "13,10,21,17,28,14,19,12,34,37,26,25,66,21,18,29,15,13,20,21,15,27"
words = re.findall(r"\d+", words)
list = []
for item in words:
  list.append(int(item))
list.sort()
print(list)
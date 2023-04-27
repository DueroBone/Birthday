import numpy, random

options = 100
options = options - 1
outFreq = 10**7
myArr = [0]

for i in range(options):
    myArr.append(0)

i = 0
while True:
    i += 1
    num = random.randint(0, options)
    myArr[num] = myArr[num] + 1
    if i % outFreq == 0:
        print(f"dev: {numpy.round((numpy.std(myArr) / numpy.sqrt(i)), 6)}, i: {i}, options: {options + 1}, spread: {numpy.max(myArr) - numpy.min(myArr)}")

import numpy, random, threading, os
from datetime import datetime

options = 100
options = options - 1
outFreq = 10**7 #was 7
myArr = numpy.zeros(options + 1, dtype=int)
reps = numpy.zeros(1, dtype=int)

def generate_numbers(length):
    inReps = 0
    theArr = numpy.zeros(options + 1, dtype=int)
    for i in range(length):
        num = random.randint(0, options)
        theArr[num] += 1
        inReps += 1
    global myArr
    global reps
    for i in range(len(myArr)):
        myArr[i] += theArr[i]
    reps[0] += inReps
    # print(".", end="")


num_threads = os.cpu_count()
# num_threads = 10
print(f"Using {num_threads} threads")
while True:
    startTime = datetime.now()
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=generate_numbers, args=(outFreq,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\ndev: {numpy.round((numpy.std(myArr) / numpy.sqrt(reps[0])), 6)}, i: {reps[0]}, options: {options + 1}, spread: {numpy.max(myArr) - numpy.min(myArr)}", end="")
    print(f" took {(datetime.now() - startTime).seconds} seconds")
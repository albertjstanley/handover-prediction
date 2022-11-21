logFolder = "./datasets/"
logFile = "act07.txt"
import time
import datetime

output = open("./datasets/processed_" + logFile, "w")
output.write("time,activity,status\n")

lastLog = ""
for line in open(logFolder + logFile, "r"):
    try:
        blocks = line.split()
        # t = datetime.datetime.strptime("2022-" + blocks[0], "%Y-%m-%d %H:%M:%S.%f")
        time = blocks[0] + " " + blocks[1]
        activity = ""
        status = ""
        if (len(blocks) >= 8 and blocks[5] == "MainActivity:" and blocks[6] == "Transition:"):
            activity = blocks[7]
            status = blocks[8][1:-1]
            o = ",".join([time, activity, status]) + "\n"
            output.write(o)
    except:
        print("line format error, ignored")

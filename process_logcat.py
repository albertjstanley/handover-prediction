logFolder = "./original/"
logFile = "test4.txt"
output = open("./testingProcess/processed_" + logFile, "w")
output.write("mRegistered,mTimeStamp,mPci,mTac,mEarfcn,mMcc+mMnc,ss,rsrp,rsrq,rssnr,cqi,ta\n")

lastLog = ""
for line in open(logFolder + logFile, "r"):
    try:
        allCellInfo = line.split("[")[1]
        individualCellInfo = allCellInfo.split(", ")
        for cellInfo in individualCellInfo:
            cellData = cellInfo.split(" ")
            if "Gsm" in cellData[0]:
                continue
            for item in cellData:
                if item.startswith("CellInfoLte:{mRegistered="):
                    mRegistered = item.split("=")[-1]
                    # print("mRegistered:", mRegistered)
                elif item.startswith("mTimeStamp="):
                    mTimeStamp = item.split("=")[1]
                    if mTimeStamp.endswith("ns"):
                        mTimeStamp = mTimeStamp[:-len("ns")]
                    # print("mTimeStamp:", mTimeStamp)
                elif item.startswith("mPci="):
                    mPci = item.split("=")[-1]
                    # print("mPci:", mPci)
                elif item.startswith("mTac="):
                    mTac = item.split("=")[-1]
                    # print("mTac:", mTac)
                elif item.startswith("mEarfcn="):
                    mEarfcn = item.split("=")[-1]
                    # print("mEarfcn:", mEarfcn)
                elif item.startswith("mMcc="):
                    mMcc = item.split("=")[-1]
                    # print("mMcc:", mMcc)
                elif item.startswith("mMnc="):
                    mMnc = item.split("=")[-1]
                    # print("mMnc:", mMnc)
                elif item.startswith("ss="):
                    ss = item.split("=")[-1]
                    # print("ss:", ss)
                elif item.startswith("rsrp="):
                    rsrp = item.split("=")[-1]
                    # print("rsrp:", rsrp)
                elif item.startswith("rsrq="):
                    rsrq = item.split("=")[-1]
                    # print("rsrq:", rsrq)
                elif item.startswith("rssnr="):
                    rssnr = item.split("=")[-1]
                    # print("rssnr:", rssnr)
                elif item.startswith("cqi="):
                    cqi = item.split("=")[-1]
                    # print("cqi:", cqi)
                elif item.startswith("ta="):
                    ta = item.split("=")[1]
                    if ta.endswith("}"):
                        ta = ta[:-len("}")]
                    # print("ta:", ta)
                    # print("1")
            
            curLog = ",".join([mRegistered, mTimeStamp, mPci, mTac, mEarfcn, mMcc + mMnc, ss, rsrp, rsrq, rssnr, cqi, ta]) + "\n"
            if curLog != lastLog:
                output.write(curLog)
            lastLog = curLog
        # print(mTimeStamp, mPci, mTac, mEarfcn, mMcc + mMnc, ss, rsrp, rsrq, rssnr, cqi, ta)
        # print(",".join([mTimeStamp, mPci, mTac, mEarfcn, mMcc + mMnc, ss, rsrp, rsrq, rssnr, cqi, ta]))
    except:
        # print("line format error, ignored")
        pass

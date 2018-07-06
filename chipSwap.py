from pprint import pprint
import sys
fileName = sys.argv[1]
ts1 = 0
data = {"QIE9_":{"word":[],"C":[],"ADC":[],"TDC":[]},\
        "QIE13":{"word":[],"C":[],"ADC":[],"TDC":[]}}
#with open('QIE9_50mV_700ns_15nsWidth_5nsTrail.txt','r') as f:
with open(fileName,'r') as f:
    for line in f:
        if not line.startswith(" #"):
            continue
        ts1 += 1
        lineList = line.split("|")
        qie9 = []
        for d in lineList[1].split(" "):
            if d != "":
                qie9.append(int(d))
        data["QIE9_"]["word"].append(lineList[0])
        data["QIE9_"]["C"].append(qie9[0])
        data["QIE9_"]["ADC"].append(qie9[1])
        data["QIE9_"]["TDC"].append(qie9[2])

        qie13 = []
        for d in lineList[5].split(" "):
            if d != "":
                qie13.append(int(d))
        data["QIE13"]["word"].append(lineList[0])
        data["QIE13"]["C"].append(qie13[0])
        data["QIE13"]["ADC"].append(qie13[1])
        data["QIE13"]["TDC"].append(qie13[2])
#        if ts1 == 1:
#           pprint(lineList[0])
outFile = open("".join(["pulses_",fileName[:-4],".csv"]),"w")
ts2 = False
tdc1 = -1
adc1 = -1
cutCount = 0
#print "ADC1,TDC1,ADC2,TDC2,"
outFile.write("TS1,ADC1,TDC1,ADC2,TDC2,\n")
for ts,capID,adc,tdc in zip(data[fileName[:5]]["word"],data[fileName[:5]]["C"],data[fileName[:5]]["ADC"],data[fileName[:5]]["TDC"]):
    
    if (not tdc == 63 and adc > 10) or ts2:
        if not ts2:
            tdc1 = tdc
            adc1 = adc
            ts1 = ts
        if tdc1 == 62:
            if ts2:
                    cutCount += 1
                    #outFile.write("\n")
                    ts2 = False
                    continue
#            elif ts2:
#                outFile.write("%s,%i,%i,%i,%i,\n"%(ts1,adc1,tdc1,adc,tdc))
#                ts2 = False
#                continue
            else:
                ts2 = True
                continue
#        if not ts2:
#            tdc1 = -1
#            adc1 = -1
#        if tdc == 62:
#            if ts2:
#                if tdc1 == 62:
#                    cutCount += 1
#                    #outFile.write("\n")
#                    ts2 = False
#                    continue
#                elif not tdc1 == -1:
#                    outFile.write("%s,%i,%i,%i,%i,\n"%(ts,adc1,tdc1,adc,tdc))
#                    ts2 = False
#                    continue
#            else:
#                tdc1 = tdc
#                adc1 = adc
#                ts2 = True
#                continue
        #print adc,",",tdc
        if not ts2:
            outFile.write("%s,"%ts)
        outFile.write("%i,%i,"%(adc,tdc))
        if ts2:
            #print "\n"
            outFile.write("\n")
            ts2 = False
        else:
            ts2 = True
outFile.close()
print cutCount

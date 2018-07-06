from pprint import pprint
import sys
fileName = sys.argv[1]
ts1 = 0
qie = int(fileName[8:10].replace("_",""))
#data = {"QIE9_":{"word":[],"C":[],"ADC":[],"TDC":[]},\
#       "QIE13":{"word":[],"C":[],"ADC":[],"TDC":[]}}
data = {qie:{"word":[],"C":[],"ADC":[],"TDC":[]}}
#with open('QIE9_50mV_700ns_15nsWidth_5nsTrail.txt','r') as f:
with open(fileName,'r') as f:
    for line in f:
        if not line.startswith(" #"):
            continue
        ts1 += 1
        lineList = line.split("|")
        chData = []
        for d in lineList[qie-8].split(" "):
            if d != "":
                chData.append(int(d))
        data[qie]["word"].append(lineList[0])
        data[qie]["C"].append(chData[0])
        data[qie]["ADC"].append(chData[1])
        data[qie]["TDC"].append(chData[2])

#        if ts1 == 1:
#           pprint(lineList[0])
outFile = open("".join(["out_",fileName[:-4],".csv"]),"w")
ts2 = False
tdc1 = -1
adc1 = -1
cutCount = 0
#print "ADC1,TDC1,ADC2,TDC2,"
outFile.write("TS1,ADC1,TDC1,ADC2,TDC2,\n")
for ts,capID,adc,tdc in zip(data[qie]["word"],data[qie]["C"],data[qie]["ADC"],data[qie]["TDC"]):
    
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
            else:
                ts2 = True
                continue
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

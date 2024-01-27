#OBIS code
# Auth= 0.0.40.0.0.255
# Disconnect=0.0.96.3.10.255
# clock=0.0.1.0.0.255
#voltage=1.0.12.7.0.255

#pip3 install pyserial==3.4
import serial
import time
from serial.tools.list_ports import comports
SNRM = "7E A0 07 03 61 93 69 47 7E"
AARQ = "7E A0 4C 03 61 10 58 27 E6 E6 00 60 3E A1 09 06 07 60 85 74 05 08 01 01 8A 02 07 80 8B 07 60 85 74 05 08 02 02 AC 12 80 10 32 9A 32 33 39 32 32 32 32 32 32 32 32 32 32 32 BE 10 04 0E 01 00 00 00 06 5F 1F 04 00 00 1E 1D FF FF CC 16 7E"  #DLMS_AARQ 60=96
auth = "7E A0 2B 03 61 32 8D EB E6 E6 00 C3 01 C1 00 0F 00 00 28 00 00 FF 01 01 09 10 87 32 4A 5D 97 22 18 0E 37 8D EE 7B 05 AA 6D B1 D6 FD 7E"  # DLMS_ACTION_REQUEST C3=195
volt = "7E A0 19 03 61 54 39 98 E6 E6 00 C0 01 02 00 03 01 00 0C 07 00 FF 02 00 BC 96 7E"  # DLMS_GET_REQUEST C0=192
freq = "7E A0 19 03 61 76 29 9A E6 E6 00 C0 01 02 00 03 01 00 0E 07 00 FF 02 00 EA 9E 7E"
current="7E A0 19 03 61 98 59 94 E6 E6 00 C0 01 02 00 03 01 00 5B 07 00 FF 02 00 0C CA 7E"
cumEngKwh="7E A0 19 03 61 54 39 98 E6 E6 00 C0 01 C1 00 03 01 00 01 08 00 FF 02 00 32 68 7E"
clock="7E A0 19 03 61 BA 49 96 E6 E6 00 C0 01 C1 00 08 00 00 01 00 00 FF 02 00 60 1A 7E"
disconnect= "7E A0 07 03 61 53 65 81 7E"


dlmsFrame = [SNRM,AARQ,auth,volt,freq,current,cumEngKwh,disconnect]
########################## send frame to meter##################
i=0
for joinFrame in dlmsFrame:
    joinFrame=''.join(joinFrame.split(' '))
    dlmsFrame[i]=joinFrame
    i=i+1


for x in comports():
    device = x.device
    print(device)



receiveFrame = []
data=[]
i=0
ser=serial.Serial('/dev/ttyUSB0')
for string in dlmsFrame:
    ser.write(bytes.fromhex(string))
    time.sleep(1)
    receiveFrame.append(ser.read_all().hex())
    frame = receiveFrame[i]
    print(frame)
    tempTx = string[32:44]
    if(tempTx == "01000C0700FF"):
        print("voltage is : ", (int(frame[32:40], 16)) / 100)
    if(tempTx == "01000E0700FF"):
        print("Frequence is : ", (int(frame[32:40], 16)) / 1000)
    if(tempTx == "01005B0700FF"):
        print("current is : ", (int(frame[32:40], 16)) / 1000)
    if (tempTx == "0000010000FF"): # for time calculation
        j = 0
        temp = []
        while j < len(frame):
            temp.append(frame[j:j + 2])
            j = j + 2
        year = int((temp[17] + temp[18]), 16)
        month = int(temp[19], 16)
        day = int(temp[20], 16)
        dayOfweak = int(temp[21], 16)
        hour = int(temp[22], 16)
        minute = int(temp[23], 16)
        second = int(temp[24], 16)
        print('{}/{}/{}'.format(day, month, year))
        print('{}:{}:{}'.format(hour, minute, second))

    i=i+1

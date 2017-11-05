import glob
import datetime
import pprint
from os.path import join, exists
from os import remove, makedirs

def getSetTimeFmt():
    dt_fmt = datetime.datetime.now().strftime("%Y%m%d")
    tm_fmt = int(datetime.datetime.now().strftime("%H%M"))

    #tm_fmt = 1210

    tm_round_fmt = [100000, 103000, 110000, 113000, 120000, 123000, 143000, 150000, 153000, 160000, 163000]

    if tm_fmt < 1030:
        dttm_fmt = dt_fmt + tm_round_fmt[0].__str__()
    elif tm_fmt < 1100:
        dttm_fmt = dt_fmt + tm_round_fmt[1].__str__()
    elif tm_fmt < 1130:
        dttm_fmt = dt_fmt + tm_round_fmt[2].__str__()
    elif tm_fmt < 1200:
        dttm_fmt = dt_fmt + tm_round_fmt[3].__str__()
    elif tm_fmt < 1230:
        dttm_fmt = dt_fmt + tm_round_fmt[4].__str__()
    elif tm_fmt < 1430:
        dttm_fmt = dt_fmt + tm_round_fmt[5].__str__()
    elif tm_fmt < 1500:
        dttm_fmt = dt_fmt + tm_round_fmt[6].__str__()
    elif tm_fmt < 1530:
        dttm_fmt = dt_fmt + tm_round_fmt[7].__str__()
    elif tm_fmt < 1600:
        dttm_fmt = dt_fmt + tm_round_fmt[8].__str__()
    elif tm_fmt < 1630:
        dttm_fmt = dt_fmt + tm_round_fmt[9].__str__()
    else:
        dttm_fmt = dt_fmt + tm_round_fmt[10].__str__()

    return dttm_fmt

""" SET STANDARD FORMAT 
C:[0] SYMBOL
C:[1] OPEN
C:[2] HIGH
C:[3] LOW
C:[4] CLOSE
C:[5] CHANGE
C:[6] CHANGE_PERCENT
C:[7] BID
C:[8] OFFER
C:[9] VOLUMN
C:[10] VALUE_000BAHT
"""

input_path = "..\\..\\datafile\\TEMP\\SEC_SET_ROUND_SOURCE"
dttm_round = getSetTimeFmt()

read_files = glob.glob(input_path + "\\" + dttm_round + "_*.csv")

output_path = "..\\..\\datafile\\SET\\ROUND_ALL"
output_file_name = output_path + "\\" + dttm_round + "_ALL_SYMBOL.csv"

#    remove(csv_file)
if exists(output_path) == False:
    makedirs(output_path)
if exists(output_file_name):
    remove(output_file_name)

print("..... Start Job .....")
print("----------------------------------------------------------------")
print("   SOURCE PATH  : ")
pprint.pprint(read_files)
print("   TARGET PATH  : ", output_file_name)


with open(output_file_name, "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            infile.readline()
            outfile.write(infile.read())

print("----------------------------------------------------------------")
print("..... End Job .....")

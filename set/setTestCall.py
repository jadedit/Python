import time
import datetime

print("Hello Everybody.", time.time())

def getSetTimeFmt():
    dt_fmt = datetime.datetime.now().strftime("%Y%m%d")
    tm_fmt = int(datetime.datetime.now().strftime("%H%M"))

    tm_round_fmt = [100000, 103000, 110000, 113000, 120000, 123000, 150000, 153000, 160000, 163000]

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
    elif tm_fmt < 1500:
        dttm_fmt = dt_fmt + tm_round_fmt[5].__str__()
    elif tm_fmt < 1530:
        dttm_fmt = dt_fmt + tm_round_fmt[6].__str__()
    elif tm_fmt < 1600:
        dttm_fmt = dt_fmt + tm_round_fmt[7].__str__()
    elif tm_fmt < 1630:
        dttm_fmt = dt_fmt + tm_round_fmt[8].__str__()
    else:
        dttm_fmt = dt_fmt + tm_round_fmt[9].__str__()

    print(dttm_fmt)

    return  dttm_fmt

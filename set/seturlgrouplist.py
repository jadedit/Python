import urllib
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from os.path import join, exists
from os import remove, makedirs
import datetime
import time
import random

# Example url
# https://www.set.or.th/set/historicaltrading.do?symbol=BBL&page=2&language=en&country=US&type=trading
# https://www.set.or.th/set/historicaltrading.do?symbol=AAV&ssoPageId=2&language=th&country=TH
# http://www.settrade.com/C13_MarketSummary.jsp?detail=INDUSTRY&order=N&industry=TECH&sector=&market=SET&sectorName=I_TECH
# https://www.settrade.com/C13_MarketSummary.jsp?detail=INDUSTRY&industry=TECH&market=SET
# https://www.settrade.com/C13_MarketSummary.jsp?detail=INDUSTRY&industry=SERVICE&market=SET

def getTableData(symbol, page=1):
    if page > 1:
        page = 1 # limit at 3

    #url_string = "https://www.set.or.th/set/historicaltrading.do?symbol={0}".format(symbol)
    #url_string += '&page={0}&language=en&country=US&type=trading'.format(page - 1)

    url_string = "https://www.settrade.com/C13_MarketSummary.jsp?detail=INDUSTRY"
    url_string += '&industry={0}&market=SET'.format(symbol)

    page = urllib.request.urlopen(url_string).read()
    soup = BeautifulSoup(page, 'lxml')
    #table_element = soup.find('table', class_='table table-info table-hover')

    table_element_all = soup.findAll('table', class_='table table-info table-hover')

    for table_element_loop in table_element_all:
        table_element = table_element_loop

        #print(table_element_loop)

    #print(table_element)

    return table_element, url_string

#table table-hover table-info
#table table-info table-hover

def createDataFrame(table_element):
    row_list = []
    head_list = []

    if table_element is None:
        return None

    tr_list = table_element.findAll('tr')

    for tr in tr_list:
        th_list = tr.findAll('th')
        if th_list is not None:
            for th in th_list:
                head_list.append(th.find(text=True))

        td_list = tr.findAll('td')

        for td in td_list:
            row_list = np.append(row_list, td.find(text=True))

    num_col = len(head_list)
    total_col = int(len(row_list) / num_col)
    row_list = np.reshape(row_list, (total_col, num_col))
    df = pd.DataFrame(columns=head_list, data=row_list)
    return df

def create_all_data(symbol, total_page=1):
    # get stock data from set.or.th web (total page)
    df = None
    for p in range(1, total_page + 1):
        table_element, url_string = getTableData(symbol, page=p)
        # print(url_string)
        df_temp = createDataFrame(table_element)
        if df is None:
            df = df_temp
        else:
            df = df.append(df_temp)
    return df

def getSetTimeFmt():
    dt_fmt = datetime.datetime.now().strftime("%Y%m%d")
    tm_fmt = int(datetime.datetime.now().strftime("%H%M"))

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

    # print(dttm_fmt)
    return dttm_fmt

#----- FILE & DIRECTORY
DIR_SEC_CSV = "..\\..\\datafile\\TEMP\\SEC_SET_ROUND_SOURCE"

def writeCSVFile(df, symbol, dttm_round, output_path=DIR_SEC_CSV, include_index=False):
    file_name = dttm_round + "_" + symbol
    csv_file = "{}.csv".format(join(output_path, file_name))
    df.to_csv(csv_file, index=include_index)

def removeOldFile(symbol, dttm_round, output_path=DIR_SEC_CSV):
    file_name = dttm_round + "_" + symbol
    csv_file = "{}.csv".format(join(output_path, file_name))

    if exists(output_path) == False:
        makedirs(output_path)
    if exists(csv_file):
        remove(csv_file)

if __name__ == "__main__":
    symbol_list = [ 'AGRI', 'FOOD', 'FASHION', 'HOME', 'PERSON', \
                    'BANK', 'FIN', 'INSUR', 'AUTO', 'IMM', 'PAPER', \
                    'PETRO', 'PKG', 'STEEL', 'CONMAT', 'PROP', 'PF%26REIT', \
                    'CONS', 'ENERG', 'MINE', 'COMM', 'HELTH', 'MEDIA', \
                    'PROF', 'TOURISM', 'TRANS', 'ETRON', 'ICT']

    print(datetime.datetime.now().strftime("%Y%m%d %H%M%S :  --- Start. ---"))

    for symbol in symbol_list:
        dttm_cmd = datetime.datetime.now().strftime("%Y%m%d %H%M%S :  ")
        dttm_round = getSetTimeFmt()

        print(dttm_cmd + symbol)
        df = create_all_data(symbol, total_page=1)

        #print(df.tail());
        # clear old files
        removeOldFile(symbol, dttm_round)
        writeCSVFile(df, symbol, dttm_round)

        #tr = random.randrange(5) + random.randrange(5)
        #time.sleep(tr)

    print(datetime.datetime.now().strftime("%Y%m%d %H%M%S :  --- End. ---"))
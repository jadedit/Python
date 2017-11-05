# pip install psycopg2

import psycopg2
import sys
import pprint

def main():
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='db201709'"
    # print the connection string we will use to connect
    print
    "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # execute our Query
    #cursor.execute("SELECT * FROM settrade.settrade_price limit 100")

    cursor.execute("SELECT \"TK_NAME\", count(*) FROM settrade.settrade_price group by 1 order by 1 limit 100")
    # retrieve the records from the database
    records = cursor.fetchall()

    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.

    #pprint.pprint(records)

    print(records)
    pprint.pprint(records)

if __name__ == "__main__":
    main()

import ptt_board_url as ptt
import pandas as pd
import psycopg2 as pg
import time

hoturl = 'https://www.ptt.cc/bbs/hotboards.html'
hot_board = ptt.get_js_page(hoturl)
hot_num = len(hot_board)
# get url
hot_board_url = ptt.get_url(hot_board, hot_num)

# get nuser
hot_board_nuser = ptt.get_nuser(hot_board, hot_num)

# get class
hot_board_classify = ptt.get_class(hot_board, hot_num)

# get board name
hot_board_name = ptt.get_boardname(hot_board, hot_num)

# get title
hot_board_title = ptt.get_title(hot_board, hot_num)

# get datetime
timenow = time.localtime()
datetimeNow = time.strftime("%Y-%m-%d %H:%M:%S", timenow)
# datetimeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # import datetime

hot_board_df = pd.DataFrame({
    'board_classify':hot_board_classify,
    'board_name':hot_board_name,
    'board_nuser':hot_board_nuser,
    'board_title':hot_board_title,
    'board_url':hot_board_url,
    'get_datetime':datetimeNow
})

print('hot_board_df: ', hot_board_df)

# connect to postgreSQL :
connect_str = " dbname = 'pttdb' user = 'amber' host = 'localhost' password = 'ww211214' "
conn = pg.connect(connect_str)
cur = conn.cursor()


##############
# https://www.ryanbaumann.com/blog/2016/4/30/python-pandas-tosql-only-insert-new-rows
# https://nelsonslog.wordpress.com/2015/04/27/inserting-lots-of-data-into-a-remote-postgres-efficiently/
##############

# prepare query
sql1 = """INSERT INTO hotboard_user_number (
                            board_classify, 
                            board_name,
                            board_nuser,
                            board_title,
                            board_url,
                            get_datetime) 
            VALUES (%s, %s, %s, %s, %s, %s); """

data1 = hot_board_df

# Execute a command
cur.execute(sql1, data1)

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test;")
cur.fetchone()

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

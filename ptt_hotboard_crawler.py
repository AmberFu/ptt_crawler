import ptt_board_url as ptt
import pandas as pd
# import sqlite3
# from firebase import firebase
# from mysql import connector
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

hot_board_df = pd.DataFrame({
    'board_name':hot_board_name,
    'board_title':hot_board_title,
    'board_classify':hot_board_classify,
    'board_nuser':hot_board_nuser,
    'board_url':hot_board_url
})

print('hot_board_df : ', hot_board_df)

df = []
# get into board
for board_name in hot_board_name:
    print('start time : ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print('board name : ', board_name)
    content = ptt.get_into_board(board_name)
    # next_url = ptt.ptt_content_to_url(content)
    r_ent_df = ptt.ptt_content_to_title(content)
    df.append(r_ent_df)
    print('--------------')
    print('r_ent_df : ', r_ent_df)
    print('end time : ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

print('df = ', df)
print('df[title]:', df['title'])
# # connect to postgreSQL :
# connect_str = " dbname = 'pttdb' user = 'amber' host = 'localhost' password = 'ww211214' "
# conn = pg.connect(connect_str)
# cur = conn.cursor()
# cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))   # Execute a command
#
# # Query the database and obtain data as Python objects
# cur.execute("SELECT * FROM test;")
# cur.fetchone()
#
# # Make the changes to the database persistent
# conn.commit()
#
# # Close communication with the database
# cur.close()
# conn.close()


######### Other database ##################
# connect to sqlite3
# conn = sqlite3.connect('ptt_hotboard_article_title')

# connect to firebase :
# fireDBurl = "https://py-ptt.firebaseio.com/"
# fdb = firebase.FirebaseApplication(fireDBurl, None)

# connect to mysql :
# db = connector.connect(
#     host = 'localhost',
#     user = 'amber',
#     password = 'ww211214',
#     database = 'ambermysqldb'
# )
# cur = db.cursor()
##########################################
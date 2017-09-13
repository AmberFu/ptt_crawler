import ptt_board_url as ptt
# import pandas as pd
# import psycopg2 as pg
import time


hoturl = 'https://www.ptt.cc/bbs/hotboards.html'
hot_board = ptt.get_js_page(hoturl)
hot_num = len(hot_board)

# get board name
hot_board_name = ptt.get_boardname(hot_board, hot_num)

# get datetime
timenow = time.localtime()
datetimeNow = time.strftime("%Y-%m-%d %H:%M:%S", timenow)

#########
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
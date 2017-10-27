import ptt_board_url as ptt
import pandas as pd
# import datetime
import sys
# import psycopg2 as pg
import time

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

hoturl = 'https://www.ptt.cc/bbs/hotboards.html'
hot_board = ptt.get_js_page(hoturl)
df = ptt.get_hotboard_df(hot_board)

end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print('start time : ', start_time)
print('end time : ', end_time)

# # print('\nresult_df = ', result_df)
# try:
#     outputFile = 'ptt_hotboard_' + str(datetime.datetime.today().strftime('%Y-%m-%d')) + '.csv'
#     df.to_csv(outputFile, sep=',', encoding='utf-8')
# except:
#     print("Unexpected error:", sys.exc_info()[0])






# # connect to postgreSQL :
# pwd = input(">>> keyin your password: ")
# try:
#     connect_str = " dbname = 'pttdb' user = 'amber' host = 'localhost' password = '" + pwd + "'"
#     conn = pg.connect(connect_str)
#     print('Prepare to write into database...')
# except:
#     print("Unable to connect to the postgreSQL!")
#
# cur = conn.cursor()
#
# try:
#     # prepare query
#     sql1 = """INSERT INTO hotboard_article_title (
#                             board,
#                             nrec,
#                             mark,
#                             title,
#                             href,
#                             author,
#                             dates,
#                             get_time)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
#
#     for n in range(len(df)):
#         cur.execute(sql1, (df.get_value(n, 'board'),
#                            df.get_value(n, 'nrec'),
#                            df.get_value(n, 'mark'),
#                            df.get_value(n, 'title'),
#                            df.get_value(n, 'href'),
#                            df.get_value(n, 'author'),
#                            df.get_value(n, 'dates'),
#                            df.get_value(n, 'get_time')))
#     print('Insert sucessfully!')
# except:
#     print('Can not execute query!')
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
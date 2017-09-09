# -*- coding: utf-8 -*-

import ptt_board_url as pt

# 將PTT所有版連結網址爬下來:
PPT = 'https://www.ptt.cc'
boardlvl1 = '/cls/1'
url = PPT + boardlvl1

# get lvl1 a_board
a_board = pt.get_a_board(url)
board_num = len(a_board)
print('Lvl1 board num: ', board_num)

# get lvl1 url :
board_lvl1_href = pt.get_url(a_board, board_num)


# get lvl2 a_board :
for lvl2_url in board_lvl1_href:
    a_board_lvl2 = pt.get_a_board(lvl2_url)
    board_num_lvl2 = len(a_board_lvl2)
    print('board_num_lvl2: ', board_num_lvl2)

    # get lvl2 url :
    board_lvl2_href = pt.get_url(a_board_lvl2, board_num_lvl2)
    print(board_lvl2_href)

   # get lvl3 a_board :
    for lvl3_url in board_lvl2_href:
        url_tail = lvl3_url.split('/')[3]
        url_num = lvl3_url.split('/')[4]

        # if there are lvl3 loop again, else list as final url :
        if (url_tail == 'cls') and (url_num != '357'):
            a_board_lvl3 = pt.get_a_board(lvl3_url)
            board_num_lvl3 = len(a_board_lvl3)
            print('board_num_lvl3: ', board_num_lvl3)

            # get lvl3 url :
            board_lvl3_href = pt.get_url(a_board_lvl3, board_num_lvl3)
            board_lvl3_title = pt.get_title3(a_board_lvl3, board_num_lvl3)
            board_lvl3_class = pt.get_class(a_board_lvl3, board_num_lvl3)
            print('board_lvl3_href: ', board_lvl3_href)
            print('board_lvl3_title: ', board_lvl3_title)
            print('board_lvl3_class: ', board_lvl3_class)

        else:
            print('This lvl3_url is final level: ', lvl3_url)

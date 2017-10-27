### 1. Get board Page html:
def get_js_page(url):
    from bs4 import BeautifulSoup
    from selenium import webdriver
    # driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.get(url)  # 把網址交給瀏覽器
    pagesource = driver.page_source  # 取得網頁原始碼
    soup = BeautifulSoup(pagesource, "html.parser")
    a_board = soup.find_all('a', 'board')
    return a_board

### 2. Get board dataframe:
""" 範例：
        <div class="b-ent">
            <a class="board" href="/bbs/Gossiping/index.html">
                <div class="board-name">Gossiping</div>
                <div class="board-nuser"><span class="hl f6">12533</span></div>
                <div class="board-class">綜合</div>
                <div class="board-title">&#9678;[八卦板] 快來支持你喜歡的候選人</div>
            </a>
        </div>
"""

def get_hotboard_df(hot_board):
    import pandas as pd
    import time

    url_list = []
    board_list = []
    user_num_list = []
    class_list = []
    title_list = []
    getTime_list = []

    for a in hot_board:
        # Url:
        board_href = a['href']
        board_url = 'https://www.ptt.cc' + board_href
        url_list.append(board_url)
        # board-name:
        board_name = a.find('div', 'board-name').string.strip()
        board_list.append(board_name)
        # board-nuser:
        board_nuser = a.find('div', 'board-nuser').string.strip()
        user_num_list.append(board_nuser)
        # board-class:
        board_class = a.find('div', 'board-class').string.strip()
        class_list.append(board_class)
        # board-title:
        board_title = a.find('div', 'board-title').string.strip()
        title_list.append(board_title)
        # get info time :
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        getTime_list.append(timenow)

    # Combine as a DataFrame:
    columns_order = ['board', 'nuser', 'class', 'title', 'href', 'get_time']
    boards_df = pd.DataFrame({'board': board_list,
                              'class': class_list,
                              'nuser': user_num_list,
                              'title': title_list,
                              'href': url_list,
                              'get_time': getTime_list},
                             columns = columns_order)
    return boards_df


### main():
import time
import sys

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
hoturl = 'https://www.ptt.cc/bbs/hotboards.html'
hot_board = get_js_page(hoturl)
df = get_hotboard_df(hot_board)
end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print('start time : ', start_time)
print('end time : ', end_time)

try:
    outputFile = '~/Documents/ptt_hotboards_' + str(time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())) + '.csv'
    df.to_csv(outputFile, sep=',', encoding='utf-8')
except:
    print("Unexpected error:", sys.exc_info()[0])

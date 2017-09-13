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


def get_url(a_board, a_num):
    result = []
    a = 0
    while a < a_num:
        a_board_n = a_board[a]
        a_href = a_board_n['href'].split('/')[0]
        if len(a_href) == 0:
            board_href = a_board_n['href']
            board_url = 'https://www.ptt.cc' + board_href
            result.append(board_url)
            a += 1
        else:
            break
    return result


def get_title(a_board, a_num):
    result = []
    a = 0
    while a < a_num:
        a_board_n = a_board[a]
        a_href = a_board_n['href'].split('/')[0]
        if len(a_href) == 0:
            board_title = a_board_n.find('div', 'board-title').string.strip()
            result.append(board_title)
            a += 1
        else:
            break
    return result


def get_title3(a_board, a_num):
    result = []
    a = 0
    while a < a_num:
        a_board_n = a_board[a]
        a_href = a_board_n['href'].split('/')[0]
        if len(a_href) == 0:
            board_title = a_board_n.find('div', 'board-title').string
            result.append(board_title)
            a += 1
        else:
            break
    return result


def get_class(a_board, a_num):
    result = []
    a = 0
    while a < a_num:
        a_board_n = a_board[a]
        a_href = a_board_n['href'].split('/')[0]
        if len(a_href) == 0:
            board_class = a_board_n.find('div', 'board-class').string.strip()
            result.append(board_class)
            a += 1
        else:
            break
    return result


def get_nuser(a_board, a_num):
    result = []
    a = 0
    while a < a_num:
        a_board_n = a_board[a]
        a_href = a_board_n['href'].split('/')[0]
        if len(a_href) == 0:
            board_nuser = a_board_n.find('div', 'board-nuser').string.strip()
            result.append(board_nuser)
            a += 1
        else:
            break
    return result


def get_boardname(a_board, a_num):
    result = []
    a = 0
    while a < a_num:
        a_board_n = a_board[a]
        a_href = a_board_n['href'].split('/')[0]
        if len(a_href) == 0:
            board_nuser = a_board_n.find('div', 'board-name').string.strip()
            result.append(board_nuser)
            a += 1
        else:
            break
    return result

##### Get article :

def get_a_board(url):
    import requests
    from bs4 import BeautifulSoup
    # 發送請求
    # ex: r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    req = requests.get(url)
    if req.status_code == 200:
        # get page text
        content = req.text
        # 進行解析
        soup = BeautifulSoup(content, "html.parser")
        a_board = soup.find_all('a', 'board')
        return a_board
    else:
        print('status_code != 200')


# 取得各熱門看板第一頁:
def get_into_board(board_name):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    url = 'https://www.ptt.cc/bbs/' + board_name + '/index.html'
    load = {
        'from': '/bbs/' + board_name + '/index.html',
        'yes': 'yes'
    }
    rs = requests.session()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    res = rs.get(url)
    if res.status_code == 200:
        # get page text
        content = res.text
        return content
    else:
        print('status_code != 200')

def ptt_content_to_url(content):
    from bs4 import BeautifulSoup
    # 進行解析
    soup = BeautifulSoup(content, "html.parser")
    # get next page :
    next_page = soup.find_all('a', 'btn wide')[1]['href']
    next_page_url = 'https://www.ptt.cc' + next_page
    return next_page_url

def ptt_url_to_content(url):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    board_name = url.split('/', 3)[3]
    load = {
        'from': '/bbs/' + board_name,
        'yes': 'yes'
    }
    rs = requests.session()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    res = rs.get(url)

# 取得各版內容標題:
def ptt_content_to_title(content):
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    # 進行解析
    soup = BeautifulSoup(content, "html.parser")
    rent_soup = soup.find_all('div', 'r-ent')

    # get next page :
    # next_page = soup.find_all('a', 'btn wide')[1]['href']

    # get board name :
    board_name = soup.find('a', 'board')['href'].split('/')[2]

    # get nrec :
    nrec_lists = []
    for nrec in rent_soup:
        nrec_lists.append(nrec.find('div', 'nrec').string)

    # get mark :
    mark_lists = []
    for mark in rent_soup:
        mark_lists.append(mark.find('div', 'mark').string)

    # get title & href:
    title_lists = []
    href_lists = []
    for title in rent_soup:
        if title.find('div', 'title').a != None:
            title_lists.append(title.find('div', 'title').a.string)
            href_lists.append(title.find('div', 'title').a['href'])
        else:
            title_lists.append(title.find('div', 'title').string.strip())
            href_lists.append('None')

    # get date :
    date_lists = []
    for md in rent_soup:
        date_lists.append(md.find('div', 'date').string)

    # get author :
    author_lists = []
    for author in rent_soup:
        author_lists.append(author.find('div', 'author').string)

    # get info time :
    timenow = time.localtime()
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", timenow)

    # get r-ent info :
    r_ent_df = pd.DataFrame({ 'board': board_name,
                                'nrec': nrec_lists,
                                'mark': mark_lists,
                                'title': title_lists,
                                'href': href_lists,
                                'dates': date_lists,
                                'author': author_lists,
                              'get_time': get_time})
    return r_ent_df


import time
import pandas as pd
import sys
import random

def get_content(url):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    from_str = url.split('/', 3)[3]

    load = {
        'from': from_str,
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


def get_allPost_pageNumber(content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    # get next page :
    next_page = soup.find_all('a', 'btn wide')[1]['href']
    pageNum = next_page.split('/', 3)[3].split('.')[0]
    Num = pageNum[5:]
    return Num


def get_content_data(content):
    from bs4 import BeautifulSoup
    import time
    import pandas as pd
    # 進行解析
    soup = BeautifulSoup(content, "html.parser")
    rent = soup.find_all('div', 'r-ent')
    # get title & href:
    title_lists = []
    board_lists = []
    href_lists = []
    for title in rent:
        if title.find('div', 'title').a != None:
            title_broad = title.find('div', 'title').a.string
            # print('type of title_broad : ', type(title_broad))
            try:
                board = title_broad.split(r"(")[-1].split(r")")[0]
                title_name = title_broad.split(r"(")[0].strip()
                # print('board = ', board)
                # print('title_name = ', title_name)
            except AttributeError:
                board = 'NA'
                title_name = 'NA'
                print('AttributeError!')
            except:
                print('Unknown Error')

            title_lists.append(title_name)
            board_lists.append(board)
            href_lists.append(title.find('div', 'title').a['href'])
        else:   # all have title even if it doesn't exist
            print('Something wrong...')
    # get date :
    date_lists = []
    for md in rent:
        date_lists.append(md.find('div', 'date').string)
    # get author :
    author_lists = []
    for author in rent:
        author_lists.append(author.find('div', 'author').string)
    # get info time :
    timenow = time.localtime()
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", timenow)
    # get r-ent info :
    r_ent_df = pd.DataFrame({'board': board_lists,
                             'title': title_lists,
                             'href': href_lists,
                             'dates': date_lists,
                             'author': author_lists,
                             'get_time': get_time})
    return r_ent_df


##########
start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
allPost_url = 'https://www.ptt.cc/bbs/ALLPOST/index.html'
content = get_content(allPost_url)
data = get_content_data(content)
pageNum = int(get_allPost_pageNumber(content))

try:
    # get_num = int(input("How many pages you want to get? (input integer or 0 means get all) :"))
    # if get_num == 0:
    #     page_end = 0
    # else:
    #     page_end = pageNum - get_num
    #     print('page_end: ', page_end)

    # while pageNum > page_end :
    while pageNum > 0:
        url = 'https://www.ptt.cc/bbs/ALLPOST/index' + str(pageNum) + '.html'
        contents = get_content(url)
        df2 = get_content_data(contents)
        data = data.append(df2)
        print('pageNum = ', pageNum)
        pageNum = pageNum - 1
        # r_sec = random.random()
        # time.sleep(r_sec)

    data = data.reset_index(level = range(len(data)), drop = True)
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('start_time : ', start_time)
    print('end_time : ', end_time)

    data_name = 'PttAllPost_'+ time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + '.csv'
    print('Saving data to csv file in ~/ptt_crawler/', data_name, ' ...')
    pd.DataFrame.to_csv(data, data_name, encoding='utf-8')
    print('Finish!')
except:
    print("Something wrong! The info is...", sys.exc_info())

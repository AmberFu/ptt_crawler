# import ptt_board_url as ptt
# import pandas as pd
# import time


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
            board = title_broad.split(r"(")[1].split(r")")[0]
            title_name = title_broad.split(r"(")[0].strip()

            title_lists.append(title_name)
            board_lists.append(board)
            href_lists.append(title.find('div', 'title').a['href'])
        else:
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
    print()

    # get r-ent info :
    r_ent_df = pd.DataFrame({'board': board_lists,
                             'title': title_lists,
                             'href': href_lists,
                             'dates': date_lists,
                             'author': author_lists,
                             'get_time': get_time})
    return r_ent_df


###

allPost_url = 'https://www.ptt.cc/bbs/ALLPOST/index.html'
content = get_content(allPost_url)
data = get_content_data(content)
pageNum = get_allPost_pageNumber(content)

for i in range(pageNum):
    print('i = ', i)


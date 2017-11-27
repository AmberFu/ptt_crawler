# 目標：針對特定看版，定時抓取文章。 python3 ptt_board_content.py -b 'lesbain' (固定抓取一天)
import getopt
import datetime
import sys
from termcolor import colored

# 取得各版第一頁內容:
def get_into_board(url):
    import requests
    import urllib3
    # from requests.packages.urllib3.exceptions import InsecureRequestWarning
    board_name = url.split('/')[4]
    load = {
        'from': '/bbs/' + board_name + '/index.html',
        'yes': 'yes'
    }
    # For GET:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Host': 'www.ptt.cc',
        'Connection': 'keep-alive',
    }
    rs = requests.session()
    urllib3.disable_warnings()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    res = rs.get(url,headers=headers)
    if res.status_code == 200:
        # get page text
        content = res.text
        return content
    else:
        print('status_code != 200')




# 取得下一頁URL:
def get_next_url(content):
    from bs4 import BeautifulSoup
    # 進行解析
    soup = BeautifulSoup(content, "html.parser")
    # get next page :
    next_page = soup.find_all('a', 'btn wide')[1]['href']
    next_page_url = 'https://www.ptt.cc' + next_page
    return next_page_url




# 取得各版內容標題:
def get_content_title(content):
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    # 進行解析
    soup = BeautifulSoup(content, "html.parser")
    rent_soup = soup.find_all('div', 'r-ent')
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
    r_ent_df_order = ['board', 'nrec', 'mark', 'title', 'href', 'dates', 'author', 'get_time']
    r_ent_df = pd.DataFrame({ 'board': board_name,
                                'nrec': nrec_lists,
                                'mark': mark_lists,
                                'title': title_lists,
                                'href': href_lists,
                                'dates': date_lists,
                                'author': author_lists,
                              'get_time': get_time}, columns = r_ent_df_order)
    return r_ent_df


# Get artile:
def get_article(href_list):
    from bs4 import BeautifulSoup
    import pandas as pd
    article_df_order = ['href', 'author_name', 'article_time', 'articles']
    author_name_list = []
    article_time_list = []
    articles_list = []
    for href in href_list:
        if href == 'None':
            print('href = None!')
            author_name_list.append('None')
            article_time_list.append('None')
            articles_list.append('None')
        else:

            url = 'https://www.ptt.cc' + href.strip()
            content = get_into_board(url)
            # 進行解析
            soup = BeautifulSoup(content, "html.parser")
            main_soup = soup.find('div', id = 'main-content')
            # Get name:
            try:
                author_name = main_soup.find_all('span', 'article-meta-value')[0].string
                author_name_list.append(author_name)
            except:
                author_name_list.append('None')
            # Get date-time:
            try:
                article_time = main_soup.find_all('span', 'article-meta-value')[3].string
                article_time_list.append(article_time)
            except:
                article_time_list.append('None')
            # Get article:
            articles = ''
            for i in soup.find('div', id='main-container').stripped_strings:
                articles = articles + i
            articles_list.append(articles)

    article_df = pd.DataFrame({
        'href': href_list,
        'author_name': author_name_list,
        'article_time': article_time_list,
        'articles': articles_list
    }, columns = article_df_order)
    # print(article_df)
    return article_df



# 3. get max_date and min_date: the newest article is at end of list.
def get_max_min_date(content):
    import datetime
    from bs4 import BeautifulSoup
    # 進行解析
    soup = BeautifulSoup(content, "html.parser")
    # get date :
    rent = soup.find_all('div', 'r-ent')
    date_lists = []
    for md in rent:
        date_lists.append(md.find('div', 'date').string)

    today_date = datetime.date.today()
    this_year = today_date.year

    # put today.year as year: if max = 2018/01/02, min = 2017/12/30 ~> 2018/12/30, today = 2018/01/05
    max_date = '{}/{}'.format(this_year, date_lists[-1].strip())
    max_date_day = datetime.datetime.strptime(max_date, '%Y/%m/%d').date()

    min_date = '{}/{}'.format(this_year, date_lists[0].strip())
    min_date_day = datetime.datetime.strptime(min_date, '%Y/%m/%d').date()

    # get diff of day:
    diff_day = (max_date_day - min_date_day).days
    # print('diff_day: ', diff_day)

    # check cross year issue: (In ALLPOST page, today must >= those dates.)
    if today_date < min_date_day:
        print('\ntoday_date - min_date_day < 0:')
        if diff_day >= 0: # min == max OR min < max ~~> both cross one year.(ex: min 2017/12/30, max 2017/12/31)
            print('max:', max_date_day, ' == min: ', min_date_day)
            max_date_day = max_date_day.replace(year = max_date_day.year - 1)
            min_date_day = min_date_day.replace(year = min_date_day.year - 1)
            diff_day = (max_date_day - min_date_day).days
        elif diff_day < 0: # if min > max ~~> only min cross one year.
            min_date_day = min_date_day.replace(year=min_date_day.year - 1)
            diff_day = (max_date_day - min_date_day).days
        else:
            print('Something wrong. Please check function: get_max_min_date() !')

        print('max:', max_date_day, ', min: ', min_date_day, 'new diff: ', diff_day)

    max_min_date = [max_date_day, min_date_day]
    return max_min_date

###########
def get_2_day(board_index_url):
    index_content = get_into_board(board_index_url)
    # NEXT URL:
    next_url = get_next_url(index_content)
    pages_num = next_url.split('/')[5].split('index')[1].split('.html')[0]
    board = next_url.split('/')[4]

    # GET index DataFrame:
    r_ent_df = get_content_title(index_content)
    article_df = get_article(r_ent_df.href)
    # JOIN index two DF:
    r_ent_df = r_ent_df.join(article_df.set_index('href'), on = 'href')

    print('\nr_ent_df = ', r_ent_df)
    print('\nnext_url = ', next_url)
    today_date = datetime.date.today()

    for i in range(int(pages_num),-1,-1):
        url = 'https://www.ptt.cc/bbs/' + board.strip() + '/index' + str(i).strip() + '.html'
        content = get_into_board(url)
        max_min_date = get_max_min_date(content)
        diff_day = (today_date - max_min_date[1]).days # compair with page's min date

        print('\nmax_min_date[1] = ', max_min_date[1])
        print('\ndiff_day = ', diff_day)

        if diff_day > 2:
            break
        elif diff_day < 0:
            print('Something wrong in get_2_day function!')
        else:
            board_df = get_content_title(content)
            arti_df = get_article(board_df.href)
            board_df = board_df.join(arti_df.set_index('href'), on = 'href')
            r_ent_df.append(board_df,ignore_index=True)
    return r_ent_df


    ###

##########







def main():
    import pandas as pd

    start_time = datetime.datetime.today()
    ### get arg from Comment Line:
    try:
        # get comment line input:
        opts, operands = getopt.getopt(sys.argv[1:], 'hb:')
        print('opts = ', opts)
        print('operands = ', operands)
    except getopt.GetoptError:
        print(colored("""
        Something wrong... Please Check your syntax:
            python3 ptt_board_content.py -b < A PTT Board Name : String >
        Or input help comment to see more detail:
            python3 ptt_board_content.py -h
        """, 'red'))
        sys.exit(2)
    except IndexError:  # if user don't input arg.
        print(colored("""
        Some arguments miss... Please Check your syntax: 
            python3 ptt_board_content.py -b < A PTT Board Name : String >
        Or input help comment to see more detail:
            python3 ptt_board_content.py -h
        """, 'red'))
        sys.exit(2)

    for o, v in opts:
        if o == '-h':
            print(colored("""
            python3 ptt_board_content.py -b < A PTT Board Name : String >
                -h : get help message.
                -b : Which PTT Board you want to crawler? (input the board name, like Gossiping...ect.)
                    The crawler will get 2 day data. (this day and the day befor this day)
            """, "blue"))
            sys.exit()

    # Get the board index pages:
    board_name = opts[0][1]
    board_index_url = 'https://www.ptt.cc/bbs/'+str(board_name).strip()+'/index.html'

    # index_content = get_into_board(board_index_url)
    # # NEXT URL:
    # next_url = get_next_url(index_content)
    #
    # # GET DataFrame:
    # r_ent_df = get_content_title(index_content)
    # article_df = get_article(r_ent_df.href)
    # # JOIN two DF:
    # r_ent_df = r_ent_df.join(article_df.set_index('href'), on = 'href')
    #
    # print('\nr_ent_df = ', r_ent_df)
    # print('\nnext_url = ', next_url)

    ###
    r_ent_df = get_2_day(board_index_url)
    print(r_ent_df)

    # counting time:
    end_time = datetime.datetime.today()
    time_cost = (end_time - start_time).total_seconds()
    print('\nstart time: ', start_time)
    print('\nend time: ', end_time)
    print('total cost...', time_cost, ' sec.')


if __name__ == "__main__":
    main()

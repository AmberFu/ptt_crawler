import datetime
import getopt
import sys
from termcolor import colored

### Function:

# 1. get content from url:
def get_contentSoup(url):
    import requests
    import urllib3
    from bs4 import BeautifulSoup
    from_str = url.split('/', 3)[3]
    # For over18 POST:
    load = {
        'from': from_str,
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
    res = rs.get(url, headers=headers)
    if res.status_code == 200:
        # get page text
        content = res.text
        soup = BeautifulSoup(content, "html.parser")
        return soup
    else:
        print(colored('status_code != 200', 'red'))

# 2. get max pages number from index page:
def get_total_pageNumber(soup):
    # get next page :
    next_page = soup.find_all('a', 'btn wide')[1]['href']
    pageNum = next_page.split('/', 3)[3].split('.')[0]
    Num = int(pageNum[5:]) + 1
    return Num



# 3. get max_date and min_date: the newest article is at end of list.
def get_max_min_date(soup):
    import datetime
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
    # else:
        # print('\ntoday_date > min_date_day.')

    # print('\nmin_date_day = ', min_date_day)
    # print('\nmax_date_day = ', max_date_day)
    # print('\ndiff_day = ', diff_day)
    max_min_date = [max_date_day, min_date_day]
    return max_min_date

# 4. get data:
def get_content_data(soup):
    import time
    import pandas as pd
    # 進行解析
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
                print('Some AttributeError...')
            except:
                print('Unknown Error')

            title_lists.append(title_name)
            board_lists.append(board)

            href_no = title.find('div', 'title').a['href'].split('/')[-1]
            href = '/bbs/' + board + '/' + href_no
            href_lists.append(href)

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




# 5. Check date in the page:
def crawler_allpost(maxPages, target_days):
    import pandas as pd
    df = pd.DataFrame()
    for pages in range(maxPages, 0, -1):
        page_url = 'https://www.ptt.cc/bbs/ALLPOST/index'+str(pages).strip()+'.html'
        page_soup = get_contentSoup(page_url)
        page_max_min_date = get_max_min_date(page_soup)  # return {max, min} = { [0] , [1] }
        if page_max_min_date[1] >= target_days:
            # print('Processing Page ' + str(pages) + ' ...')
            r_ent_df = get_content_data(page_soup)
            df = df.append(r_ent_df, ignore_index=True)
        elif page_max_min_date[1] < target_days and page_max_min_date[0] >= target_days:
            # print('Processing Page ' + str(pages) + ' ...')
            r_ent_df = get_content_data(page_soup)
            df = df.append(r_ent_df, ignore_index=True)
        else:
            # print('Finish!')
            break
    return df



##### main():
def main():
    start_time = datetime.datetime.today()
    ### get arg from Comment Line:
    try:
        # get comment line input:
        opts, operands = getopt.getopt(sys.argv[1:], 'hd:o:')
    except getopt.GetoptError:
        print(colored("""
        Something wrong... Please Check your syntax:
            python3 ptt_all_post_v3.py -d < how many days:int > -o < /outputFile/path >
        Or input help comment to see more detail:
            python3 ptt_all_post_v3.py -h
        """, 'red'))
        sys.exit(2)
    except IndexError:  # if user don't input arg.
        print(colored("""
        Some arguments miss... Please Check your syntax: 
            python3 ptt_all_post_v3.py -d < how many days:int > -o < /outputFile/path >
        Or input help comment to see more detail:
            python3 ptt_all_post_v3.py -h
        """, 'red'))
        sys.exit(2)

    for o, v in opts:
        if o == '-h':
            print(colored("""
            python3 ptt_all_post_v3.py -d < how many days:int > -o < /outputFile/path >
                -h : get help message.
                -d : How many day you want to crawler? (input an integer)
                        The range is from 1 to 7. (PTT ALLPOST just save 7~8 days)
                        1 for today until now, 2 for yesterday until now...ect.
                -o : output file path.
            """, "blue"))
            sys.exit()

    # For input datetime & file path:
    try:
        # date:
        int_days = opts[0][1]

        # if type(int_days) != 'int':
        #     print(colored("Input value must be integer !", 'red'))
        #     sys.exit()

        int_days = int(int_days)

        if int_days < 1:
            print(colored("Input value can't smaller than 1 !", 'red'))
            sys.exit()
        elif int_days > 7:
            print(colored("Input value can't larger than 7 !", 'red'))
            sys.exit()

        today_date = datetime.date.today()
        # Find out target day:
        target_days = today_date - datetime.timedelta(days = int_days - 1)
        print('target_days = ', target_days)
        print('\ndate_f == today_date ? ', target_days == today_date)

        # file:
        outputFile = opts[1][1]

        print('\noutputFile = ', outputFile)

    ### For PTT ALLPOST: check

        # index page: (The newest page)
        index_url = 'https://www.ptt.cc/bbs/ALLPOST/index.html'
        index_soup = get_contentSoup(index_url)

        # last page: (The oldest page)
        index1_url = 'https://www.ptt.cc/bbs/ALLPOST/index1.html'
        index1_soup = get_contentSoup(index1_url)

        # max pages:
        maxPages = get_total_pageNumber(index_soup)
        print('\nmaxPages = ', maxPages)

        # get max_date:
        max_date = get_max_min_date(index_soup)[0] # return {max, min}
        print('\nmax_date = ', max_date)

        # get min_date:
        min_date = get_max_min_date(index1_soup)[1] # return {max, min}
        print('\nmin_date = ', min_date)

        # START crawler: -> loop from maxPages and check date every page.
        result_df = crawler_allpost(maxPages, target_days)
        # print('\nresult_df = ', result_df)
        try:
            result_df.to_csv(outputFile, sep='|', encoding='utf-8')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        # counting time:
        end_time = datetime.datetime.today()
        time_cost = (end_time - start_time).total_seconds()
        print('\nstart time: ', start_time)
        print('\nend time: ', end_time)
        print('total cost...', time_cost, ' sec.')

    except ValueError: # handel date string error.
        print(colored("""
        ValueError! please check syntax:
        python3 ptt_all_post_v3.py -d < how many days:int > -o < /outputFile/path >
        
            -d how many days want to get? (input an integer)
            -o /.../outputFile/path  
        """, 'red'),
              '\n', colored("\tDetail information:", 'red'),
              '\n\t', colored(sys.exc_info()[1], 'red'))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


if __name__ == "__main__":
    main()

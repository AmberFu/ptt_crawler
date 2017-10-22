import datetime
import getopt
import sys
from termcolor import colored


# get content from url:
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

# get max pages number from index page:
def get_total_pageNumber(soup):
    # get next page :
    next_page = soup.find_all('a', 'btn wide')[1]['href']
    pageNum = next_page.split('/', 3)[3].split('.')[0]
    Num = int(pageNum[5:]) + 1
    return Num



# get max_date and min_date: the newest article is at end of list.
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
    print('diff_day: ', diff_day)

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
    else:
        print('\ntoday_date > min_date_day.')

    print('\nmin_date_day = ', min_date_day)
    print('\nmax_date_day = ', max_date_day)
    print('\ndiff_day = ', diff_day)
    max_min_date = [max_date_day, min_date_day]
    return max_min_date


# check_input_date_range:
def check_input_date_range(inputDate, minDate, maxDate):
    try:
        if inputDate > maxDate:
            print(colored("""
                    Input date out of range! \n
                    Input date must <= {} !""".format(maxDate), 'red'))
            sys.exit(2)
        elif inputDate < minDate:
            print(colored("""
                    Input date out of range! \n
                    Input date must >= {} !""".format(minDate), 'red'))
            sys.exit(2)
        else:
            print('Input is OK!')
    except SystemExit:
        print('Please try again.')
        raise
    return 0

def check_page_range(pageNum):
    guess_url = 'https://www.ptt.cc/bbs/ALLPOST/index' + str(pageNum).strip() + '.html'
    print('first url = ', guess_url)
    guess_soup = get_contentSoup(guess_url)
    guess_date_range = get_max_min_date(guess_soup)
    return guess_date_range

def comfirm_page_range(guest_date, input_date_f):
    if guest_date[0] == input_date_f and guest_date[1] == input_date_f:
        print('equal!')
        comfirm = False
    elif guest_date[0] > input_date_f and guest_date[1] == input_date_f:
        print('find the end page!')
        comfirm = True
    elif guest_date[0] > input_date_f and guest_date[1] > input_date_f:
        print('check for end page!') # if sep by same page ?! => MAYBE... +/- 1 also equal
        comfirm = False
    elif guest_date[0] == input_date_f and guest_date[1] < input_date_f:
        print('find the start page!')
        comfirm = True
    elif guest_date[0] < input_date_f and guest_date[1] < input_date_f:
        print('check for start page!') # if sep by same page ?! => MAYBE... +/- 1 also equal
        comfirm = False
    else:
        print('guest_1_date[0](max day) = ', guest_date[0])
        print('guest_1_date[1](min day) = ', guest_date[1])
        print('input_date_f = ', input_date_f)
        comfirm = False
    return comfirm

# use input date to get page range:
def get_page_range(input_date_f, min_date, max_date, maxPages):

    # count days:
    diff_day = (max_date - min_date).days + 1
    print('diff_day: ', diff_day)

    # guess pages:
    page_list = list(range(1, maxPages, maxPages // diff_day))
    print('page_list: ', page_list)

    # get list_place:
    list_place = (input_date_f - min_date).days + 1
    print('list_place: ', list_place)

    # start pages:
    start_num = page_list[list_place]
    print('start_num: ', start_num)

    # getting start page number:
    guest_1_date = check_page_range(start_num)
    print('guest_1_date = ', guest_1_date)

    # if else ...
    comfirm = comfirm_page_range(guest_1_date, input_date_f)
    print('comfirm = ', comfirm)

    # the guess quite fine, to get +1 day's page:
    # end_pageNum = start_num + 500
    # guest_2_date = check_page_range(end_pageNum)









def main():
    start_time = datetime.datetime.today()
    ### For Comment Line:
    try:
        # get comment line input:
        opts, operands = getopt.getopt(sys.argv[1:], 'hd:o:')
    except getopt.GetoptError:
        print(colored("""
        Something wrong... Please Check your syntax:
            python3 ptt_all_post_v2.py -d < yyyy/mm/dd > -o < /outputFile/path >
        Or input help comment to see more detail:
            python3 ptt_all_post_v2.py -h
        """, 'red'))
        sys.exit(2)
    except IndexError:  # if user don't input arg.
        print(colored("""
        Some arguments miss... Please Check your syntax: 
            python3 ptt_all_post_v2.py -d < yyyy/mm/dd > -o < /outputFile/path >
        Or input help comment to see more detail:
            python3 ptt_all_post_v2.py -h
        """, 'red'))
        sys.exit(2)

    for o, v in opts:
        if o == '-h':
            print("""
            ptt_all_post_v2.py -h -d < yyyy/mm/dd > -o < /outputFile/path > 
                -h : get help message.
                -d : the day you want to crawler.
                -o : the path you want to save the data.
            """)
            sys.exit()

    # For input datetime & file path:
    try:
        # date:
        input_dateStr = opts[0][1]
        input_date_f = datetime.datetime.strptime(input_dateStr, '%Y/%m/%d').date()

        today_date = datetime.date.today()
        print('\ndateStr = ', input_dateStr, '\ntype(dateStr) = ', type(input_dateStr))
        print('\ndate_f = ', input_date_f, '\ntype(date_f) = ', type(input_date_f))
        print('\ntoday of date = ', today_date, '\ntype(today_date) = ', type(today_date))
        print('\ndate_f == today_date ? ', input_date_f == today_date)


        # file:
        outputFile = opts[1][1]

        print('\noutputFile = ', outputFile)

    ### For PTT ALLPOST:

        index_url = 'https://www.ptt.cc/bbs/ALLPOST/index.html'
        index1_url = 'https://www.ptt.cc/bbs/ALLPOST/index1.html'
        # index page:
        index_soup = get_contentSoup(index_url)
        # last page:
        index1_soup = get_contentSoup(index1_url)
        # max pages:
        maxPages = get_total_pageNumber(index_soup)
        print('\nmaxPages = ', maxPages, ', type(maxPages) = ', type(maxPages))

        # get max_date:
        max_date = get_max_min_date(index_soup)[0] # return {max, min}
        print('\nmax_date = ', max_date, ', type(max_date) = ', type(max_date))

        # get min_date:
        min_date = get_max_min_date(index1_soup)[1] # return {max, min}
        print('\nmin_date = ', min_date, ', type(min_date) = ', type(min_date))

        # check input date to date range:
        check_input_date_range(input_date_f, min_date, max_date)

        # count days:
        diff_day = (max_date - min_date).days + 1
        print('diff_day: ', diff_day)

        ####### use input date to guess page range:
        # # guess pages:
        # page_list = list(range(1, maxPages, maxPages//diff_day))
        # print('page_list: ', page_list)
        #
        # # get list_place:
        # list_place = (input_date_f - min_date).days + 1
        # print('list_place: ', list_place)
        #
        # # start pages:
        # start_num = page_list[list_place]
        # print('start_num: ', start_num)
        #
        # # getting start page number:
        # guess_1_url = 'https://www.ptt.cc/bbs/ALLPOST/index'+str(start_num).strip()+'.html'
        # print('first url = ', guess_1_url)
        # guess_1_soup = get_contentSoup(guess_1_url)
        # guest_1_date = get_max_min_date(guess_1_soup)
        # print('guest_1_date = ', guest_1_date)
        output_page_range = get_page_range(input_date_f, min_date, max_date, maxPages)


        # counting time:
        end_time = datetime.datetime.today()
        time_cost = (end_time - start_time).total_seconds()
        print('\nstart time: ', start_time)
        print('\nend time: ', end_time)
        print('total cost...', time_cost, ' sec.')

    except ValueError: # handel date string error.
        print(colored("""
        ValueError! please check syntax:
        python3 ptt_all_post_v2.py -d < yyyy/mm/dd > -o < /outputFile/path >
            -d < yyyy/mm/dd >
            -o < /outputFile/path >
        """, 'red'))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == "__main__":
    main()



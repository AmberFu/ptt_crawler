import sys
import getopt
from termcolor import colored
import time

# get max pages number from index page:
def get_max_pageNumber():
    import requests as rs
    from bs4 import BeautifulSoup
    import time
    import pandas as pd

    url = 'https://www.ptt.cc/bbs/ALLPOST/index.html'
    res = rs.get(url)
    if res.status_code == 200:
        # get page text
        content = res.text
        soup = BeautifulSoup(content, "html.parser")
        # get next page :
        next_page = soup.find_all('a', 'btn wide')[1]['href']
        pageNum = next_page.split('/', 3)[3].split('.')[0]
        Num = int(pageNum[5:]) + 1
        # get date :
        currentDate = time.strftime("%Y-%m-%d", time.localtime())
        rent = soup.find_all('div', 'r-ent')
        date_lists = []
        for md in rent:
            date_lists.append(md.find('div', 'date').string)
        maxDate = date_lists[-1]
        minDate = date_lists[0]
        print('(max, min) = (', maxDate, ', ', minDate, ')')
        print('currentDate = ', currentDate)
        print('date_lists = ', date_lists)
        return Num
    else:
        print(colored('status_code != 200', 'red'))


# get content from url:
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
        print(colored('status_code != 200', 'red'))



def main():

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

    for o, v in opts:
        if o == '-h':
            print("""
                    ptt_all_post_v2.py -h -d < yyyy/mm/dd > -o < /outputFile/path > 
                        -h : get help message.
                        -d : the day you want to crawler.
                        -o : the path you want to save the data.
                    """)
            sys.exit()

    dateStr = opts[0][1]
    outputFile = opts[1][1]
    print('dateStr = ', dateStr)
    print('outputFile = ', outputFile)
    maxpages = get_max_pageNumber()
    print('maxpages = ', maxpages, ', type(maxpages) = ', type(maxpages))

if __name__ == "__main__":
    main()



import sys
from termcolor import colored

def get_into_board(url):
    import requests as rs
    res = rs.get(url)
    if res.status_code == 200:
        # get page text
        content = res.text
        return content
    else:
        print(colored('This url: ', url, '\n Status_code != 200', 'red'))


n = 5580

try:
    f = open('sixyear_tianya.txt', 'a+')

    for i in range(1, n):
        url = 'http://bbs.tianya.cn/post-motss-404641-' + str(i) + '.shtml'
        contents = get_into_board(url) + '\n\n\n##########___________##########\n\n\n'
        f.write(contents)
        print('Finish: ', i)

    f.close()
    print("It's Done!")
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
except:
    print("Unexpected error:", sys.exc_info()[0])

import requests as requests
import json
from datetime import date
import re

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# to search
query = "Um processo é uma atividade que ocorre em meio computacional, usualmente possuindo um objetivo definido, tendo duração infinita e utilizando uma quantidade limitada de recursos computacionais."

header = {'Host': 'www.qconcursos.com',
          'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5',
          'Accept-Encoding': 'identity',
          'Alt-Used': 'www.qconcursos.com',
          'Connection': 'keep-alive',
          'Cookie': '_my_app_session=',
          'Upgrade-Insecure-Requests': '1',
          'Sec-Fetch-Dest': 'document',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-Site': 'none',
          'Sec-Fetch-User': '?1',
          'Cache-Control': 'max-age=0',
          'TE': 'trailers'}


def get_code(site):
    raw = requests.get(site, headers=header).text
    init_index = raw.find('<span itemprop="position" content="4">\n<span itemprop="name">') + len(
        '<span itemprop="position" content="4">\n<span itemprop="name">')
    if init_index == -1:
        return -1
    raw = raw[init_index:]
    raw = raw[:raw.index('<')]

    return raw[1:]


def __get_next_valid_cookie__(lines):
    for line in lines[1:]:
        line_items = line.split(':')
        if int(line_items[1]) < 9:
            return "_my_app_session=" + line_items[0]
    else:
        return -1


def set_cookie():
    with open('pseudo_database.hnf', 'r+') as db:
        items = db.read().splitlines()
        if items[0] != str(date.today()):  # If the db date not today reset the counter
            db.seek(0)
            db.truncate(0)
            content = str(date.today()) + '\n' + re.sub(':[0-9]+', ':0', "\n".join(items[1:]))
            print(content)
            db.write(content)
        # set_cookie
        header['Cookie'] = __get_next_valid_cookie__(items)


def set_used_cookie(cookie, used_answers):
    cookie = cookie[len('_my_app_session='):]
    with open('pseudo_database.hnf', 'r+') as db:
        new_file = []
        for line in db.readlines()[1:]:
            if line.split(':')[0] == cookie:
                new_file.append(f"{line.split(':')[0]}:{used_answers}")
            else:
                new_file.append(line.strip())
        db.seek(0)
        db.truncate(0)
        db.write(str(date.today()) + "\n" + "\n".join(new_file))


if __name__ == "__main__":
    # query = input("Cole a pergunta: ")
    for site in search(query, tld="com", num=10, stop=10, pause=2):
        if str(site).__contains__('qconcursos') and str(site).__contains__('questoes/'):
            question_code = get_code(site)
            set_cookie()
            if header['Cookie'] == -1:
                print("Acabaram os biscoitos, arruma mais pra nós e bota no DB ae")
                pass
            response = requests.post(f'https://www.qconcursos.com/api/questions/{question_code}/answer',
                                     {'answer': 'C'}, headers=header)
            if response.status_code == 422:
                print("Cabo os request papai")
                pass

            elif response.status_code == 401:
                print("Esse cu quie ta invalido hein peste")
                pass

            else:
                response = json.loads(response.text)
                print(response['resolve']['right_answer'] if 'right_answer' in response['resolve'].keys() else 'C')
                set_used_cookie(header['Cookie'], response['used_answers'])

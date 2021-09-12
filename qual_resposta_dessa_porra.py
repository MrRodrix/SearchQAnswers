import requests as requests
import json
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
        'Cookie': '_my_app_session=ekhKYm5IclUvcG1sditUQnNSeXVoMTloTFRQN1A2bE42dzJ5UStrUGRaMHBMK1J2TXM2aVMzVUtzRUUwZndIRmRWU1FSbzc2OHc4QVAwMHZURm1YTFNseHdLTHhOeWExRnN5R200Vms5K2NVajlsbysrcUZ3aXp4YlhDczA5VU80bStFOXEwUFRSNlZlbElzYS9KaDY1bzU3L3NqMzdJdEY0SndtZk1MTFJQak1SVG5JbGJIQjBPUEhnT3hldnRpRzlUUklRcjVoejJTeTBJc25tMC9xcEhkN1BJVjJCOTBqaDhwNS9IOWh3TzJGdjM0bERTZ0xVU3VYcWJ1VVZHTzh3cEQvaVdYbkUxcmg3K1k2M2x1b0NCLzdSbTI2Q2RVYXpaSEluQXJxeUExblFaSXF2ZWZuK2ZUY1BGeHFpanBVeEZubGpPWjU4RGN2aDFGekpqcE4vRzJzUXdFYkJUcXRPR3MvVThhSVpBPS0temgwWG40bFduSkxMRjhKU1hsN3pzQT09--a6b0b054a49050bead3bd4627a6e9888608ace19;',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers'}

def get_code(site):
    raw = requests.get(site, headers=header).text
    init_index = raw.find('<span itemprop="position" content="4">\n<span itemprop="name">') + len('<span itemprop="position" content="4">\n<span itemprop="name">')
    if init_index == -1:
        return -1
    raw = raw[init_index:]
    raw = raw[:raw.index('<')]

    return raw[1:]

if __name__ == "__main__":
    for site in search(query, tld="co.in", num=10, stop=10, pause=2):
        if str(site).__contains__('qconcursos') and str(site).__contains__('questoes/'):
            question_code = get_code(site)

            response = requests.post(f'https://www.qconcursos.com/api/questions/{question_code}/answer', {'answer': 'C'}, headers=header)
            if response.status_code == 422:
                print("Cabo os request papai")
                
            elif response.status_code == 401:
                print("Cadeu teu CU quie")
            else:
                response = json.loads(response.text)
                print(response['resolve']['right_answer'] if 'right_answer' in response['resolve'].keys() else 'C')


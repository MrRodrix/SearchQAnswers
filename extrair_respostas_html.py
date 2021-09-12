import requests
from bs4 import BeautifulSoup
import json

# Data to be written
dic_file = open("questions.json", 'r')
dictionary = json.load(dic_file)
dic_file.close()

getpage = open("Questionário relativo a Conceitos de SOs (Aulas 01 a 04).html", 'r')

getpage_soup = BeautifulSoup(getpage, 'html.parser')

all_id_para1 = getpage_soup.findAll('div', {'class': 'qtext'})
answers = getpage_soup.findAll('div', {'class': 'rightanswer'})
for para in range(len(all_id_para1)):
    question = str(all_id_para1[para])
    question = question[question.index("<p>") + 3:question.index("</p>")]

    answer = str(answers[para])[48:-8 if "True" in str(answers[para]) or "False" in str(answers[para]) else -6]

    dictionary[question] = answer

dic_file = open("questions.json", 'w')
json.dump(dictionary, indent=4, fp=dic_file, ensure_ascii=False, skipkeys=False)
dic_file.close()
